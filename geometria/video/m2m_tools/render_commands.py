"""Render command construction and optional execution.

Adapted from Math-To-Manim (math_to_manim/rendering/). Pure standard library.
A missing manim/ffmpeg/ffprobe binary is reported as a skipped ToolResult, not
an exception, so these run safely in any environment and degrade to dry runs.

Use this to:
  * build the exact `manim -qh scene.py SceneName` command for each Act,
  * concatenate per-Act MP4s into the final video (replaces the hand-written
    concat.py snippet), with existence validation,
  * probe the final MP4 for duration/resolution as a render sanity check.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys


QUALITY_FLAGS = {
    "draft": "-ql", "low": "-ql", "l": "-ql",
    "medium": "-qm", "m": "-qm",
    "high": "-qh", "h": "-qh",
    "production": "-qp", "p": "-qp",
    "4k": "-qk", "k": "-qk",
}


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    skipped: bool
    command: tuple[str, ...]
    returncode: int | None = None
    stdout: str = ""
    stderr: str = ""
    reason: str | None = None
    output_path: Path | None = None
    metadata: dict[str, object] = field(default_factory=dict)


def resolve_binary(binary: str) -> str | None:
    """Return an executable path or None without raising."""

    candidate = Path(binary)
    if candidate.is_absolute() or len(candidate.parts) > 1:
        return str(candidate) if candidate.exists() else None
    return shutil.which(binary)


def quality_flag(quality: str) -> str:
    if quality.startswith("-q"):
        return quality
    try:
        return QUALITY_FLAGS[quality]
    except KeyError as exc:
        valid = ", ".join(sorted(QUALITY_FLAGS))
        raise ValueError(
            f"Unknown quality '{quality}'. Valid: {valid}") from exc


def build_manim_command(
    source_path: str | Path,
    scene_name: str | None = None,
    *,
    quality: str = "high",
    manim_bin: str = "manim",
    media_dir: str | Path | None = None,
) -> list[str]:
    """Construct the manim render command without running it. Final = -qh."""

    cmd = [manim_bin, quality_flag(quality), str(Path(source_path))]
    if scene_name:
        cmd.append(scene_name)
    if media_dir is not None:
        cmd.extend(["--media_dir", str(Path(media_dir))])
    return cmd


def render_manim_scene(
    source_path: str | Path,
    *,
    scene_name: str | None = None,
    quality: str = "high",
    media_dir: str | Path | None = None,
    manim_bin: str = "manim",
    timeout_seconds: float = 600.0,
    dry_run: bool = False,
) -> ToolResult:
    """Render one scene with the local Manim CLI if present, else skip."""

    source = Path(source_path).resolve()
    prefix = _resolve_manim_prefix(manim_bin)
    cmd = [*prefix, quality_flag(quality), str(source)] if prefix else \
        [manim_bin, quality_flag(quality), str(source)]
    if scene_name:
        cmd.append(scene_name)
    if media_dir is not None:
        Path(media_dir).mkdir(parents=True, exist_ok=True)
        cmd.extend(["--media_dir", str(Path(media_dir).resolve())])

    if not prefix:
        return ToolResult(False, True, tuple(cmd),
                          reason="manim not found on PATH")
    if dry_run:
        return ToolResult(True, True, tuple(cmd), reason="dry run")
    if not source.exists():
        return ToolResult(False, True, tuple(cmd),
                          reason=f"scene source not found: {source}")

    try:
        done = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout_seconds, check=False)
    except subprocess.TimeoutExpired as exc:
        return ToolResult(False, False, tuple(cmd), stdout=exc.stdout or "",
                          stderr=exc.stderr or "",
                          reason=f"timed out after {timeout_seconds}s")
    out = _newest_mp4(Path(media_dir)) if media_dir is not None else None
    return ToolResult(done.returncode == 0, False, tuple(cmd),
                      returncode=done.returncode, stdout=done.stdout,
                      stderr=done.stderr, output_path=out)


def write_concat_listfile(clips: Sequence[str | Path], list_path: str | Path,
                          *, validate_exist: bool = True) -> Path:
    """Write an ffmpeg concat demuxer list file. Validates clips exist first."""

    clip_paths = [Path(c) for c in clips]
    if validate_exist:
        missing = [str(c) for c in clip_paths if not c.exists()]
        if missing:
            raise FileNotFoundError(f"clips missing: {missing}")
    target = Path(list_path)
    with target.open("w", encoding="utf-8") as fh:
        for c in clip_paths:
            fh.write(f"file '{c.resolve().as_posix()}'\n")
    return target


def concat_videos(
    clips: Sequence[str | Path],
    output_path: str | Path,
    *,
    ffmpeg_bin: str = "ffmpeg",
    timeout_seconds: float = 300.0,
    dry_run: bool = False,
) -> ToolResult:
    """Concatenate per-Act MP4s into one file via the ffmpeg concat demuxer."""

    output = Path(output_path)
    binary = resolve_binary(ffmpeg_bin)
    list_path = output.with_suffix(".concat.txt")
    try:
        write_concat_listfile(clips, list_path)
    except FileNotFoundError as exc:
        return ToolResult(False, True, (), reason=str(exc), output_path=output)

    cmd = [binary or ffmpeg_bin, "-y", "-f", "concat", "-safe", "0",
           "-i", str(list_path), "-c", "copy", str(output)]
    if binary is None:
        return ToolResult(False, True, tuple(cmd), output_path=output,
                          reason=f"ffmpeg not found: {ffmpeg_bin}")
    if dry_run:
        return ToolResult(True, True, tuple(cmd), output_path=output,
                          reason="dry run")
    try:
        done = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout_seconds, check=False)
    except subprocess.TimeoutExpired as exc:
        return ToolResult(False, False, tuple(cmd), stdout=exc.stdout or "",
                          stderr=exc.stderr or "", output_path=output,
                          reason=f"timed out after {timeout_seconds}s")
    return ToolResult(done.returncode == 0 and output.exists(), False,
                      tuple(cmd), returncode=done.returncode,
                      stdout=done.stdout, stderr=done.stderr,
                      output_path=output,
                      reason=None if done.returncode == 0 else "ffmpeg failed")


def probe_video(video_path: str | Path, *, ffprobe_bin: str = "ffprobe",
                timeout_seconds: float = 30.0) -> dict:
    """Return basic ffprobe metadata if ffprobe is present, else a skip dict."""

    path = Path(video_path)
    binary = resolve_binary(ffprobe_bin)
    cmd = (binary or ffprobe_bin, "-v", "error", "-show_format",
           "-show_streams", "-of", "json", str(path))
    if binary is None:
        return {"ok": False, "skipped": True, "reason": "ffprobe not found"}
    if not path.exists():
        return {"ok": False, "skipped": True, "reason": f"not found: {path}"}
    try:
        done = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout_seconds, check=False)
    except subprocess.TimeoutExpired:
        return {"ok": False, "skipped": False, "reason": "ffprobe timed out"}
    if done.returncode != 0:
        return {"ok": False, "skipped": False, "reason": "ffprobe failed",
                "stderr": done.stderr}
    try:
        raw = json.loads(done.stdout or "{}")
    except json.JSONDecodeError:
        return {"ok": False, "skipped": False, "reason": "bad ffprobe json"}
    fmt = raw.get("format", {})
    vstream = next((s for s in raw.get("streams", [])
                    if s.get("codec_type") == "video"), {})
    return {
        "ok": True, "skipped": False,
        "duration_seconds": float(fmt["duration"]) if "duration" in fmt else None,
        "width": vstream.get("width"),
        "height": vstream.get("height"),
    }


def _resolve_manim_prefix(manim_bin: str) -> tuple[str, ...]:
    for cand in ((manim_bin,), (sys.executable, "-m", "manim")):
        binary = resolve_binary(cand[0])
        if binary is not None:
            return (binary, *cand[1:])
    return ()


def _newest_mp4(media_dir: Path | None) -> Path | None:
    if media_dir is None or not media_dir.exists():
        return None
    videos = [p for p in media_dir.rglob("*.mp4") if p.is_file()]
    return max(videos, key=lambda p: p.stat().st_mtime) if videos else None
