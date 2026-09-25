"""The static gate: the runnable check that must pass before any render.

This is the concrete implementation of SKILL.md PART VII §7.4. It parses a
generated scene file (no execution, no Manim install needed), runs the security
+ Manim-anti-pattern validator, discovers the Scene classes, and prints a
report plus the exact render commands. Exits nonzero on any error so it can
gate a render in a shell pipeline.

Run:
    python -m m2m_tools.gate path/to/generated_scene.py
    python -m m2m_tools.gate scene.py --quality h --media-dir media

Or call run_gate(path) from Python and inspect the returned dict.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ast_validation import validate_scene_source
from .scene_discovery import discover_scene_classes
from .render_commands import build_manim_command


def run_gate(path: str | Path, *, quality: str = "h",
             media_dir: str | None = None) -> dict:
    """Validate and inspect a scene file. Returns a result dict; does not render."""

    src_path = Path(path)
    source = src_path.read_text(encoding="utf-8")

    result = validate_scene_source(source, filename=str(src_path))
    scenes = discover_scene_classes(source, filename=str(src_path),
                                    require_construct=True)
    scene_names = [s.name for s in scenes]
    commands = [
        build_manim_command(src_path, name, quality=quality, media_dir=media_dir)
        for name in scene_names
    ]
    return {
        "ok": result.ok and bool(scene_names),
        "validation": result,
        "scene_names": scene_names,
        "render_commands": commands,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Static gate for generated Manim scenes (no render).")
    parser.add_argument("scene", help="path to the generated .py scene file")
    parser.add_argument("--quality", default="h",
                        help="render quality flag for the printed commands")
    parser.add_argument("--media-dir", default=None,
                        help="optional --media_dir for the printed commands")
    args = parser.parse_args(argv)

    try:
        res = run_gate(args.scene, quality=args.quality, media_dir=args.media_dir)
    except FileNotFoundError:
        print(f"gate: file not found: {args.scene}", file=sys.stderr)
        return 2
    except SyntaxError as exc:
        print(f"gate: cannot parse: {exc}", file=sys.stderr)
        return 1

    print(res["validation"].report())
    if res["scene_names"]:
        print("\nScenes discovered:")
        for name in res["scene_names"]:
            print(f"  - {name}")
        print("\nRender commands:")
        for cmd in res["render_commands"]:
            print("  " + " ".join(cmd))
    else:
        print("\nERROR: no construct-bearing Scene classes found.")

    if not res["ok"]:
        print("\nGate FAILED. Fix the script before rendering.", file=sys.stderr)
        return 1
    print("\nGate PASSED. Safe to render.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
