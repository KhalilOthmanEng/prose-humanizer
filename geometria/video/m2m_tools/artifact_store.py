"""Small content-addressed artifact store for inspectable planning bundles.

Ported and trimmed from Math-To-Manim (math_to_manim/tools/artifact_store.py).
Pure standard library. Writes the planning ladder's rungs (intent, knowledge
graph, curriculum, math packet, storyboard, scene spec) and the validation and
render results to a run directory as JSON, so every step is inspectable before
and after code. This is the "typed artifacts first" discipline made concrete.

Typical layout written under <root>/:
    manifest.json
    artifacts/<hash>-intent.json
    artifacts/<hash>-knowledge_graph.json
    ...
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
from typing import Any


class ArtifactStoreError(RuntimeError):
    """Raised when the store cannot read or write its manifest."""


@dataclass(frozen=True)
class Artifact:
    id: str
    path: Path
    kind: str
    sha256: str
    size_bytes: int
    metadata: Mapping[str, Any]


class ArtifactStore:
    """A deterministic local store keyed by content hash and safe names."""

    manifest_name = "manifest.json"

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.artifacts_dir = self.root / "artifacts"
        self.manifest_path = self.root / self.manifest_name
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self._manifest = self._load_manifest()

    def put_json(self, value: Any, name: str, *, kind: str = "json",
                 metadata: Mapping[str, Any] | None = None) -> Artifact:
        data = json.dumps(value, indent=2, sort_keys=True, default=str)
        return self.put_bytes(data.encode("utf-8"), name, kind=kind,
                              metadata=metadata)

    def put_text(self, text: str, name: str, *, kind: str = "text",
                 metadata: Mapping[str, Any] | None = None) -> Artifact:
        return self.put_bytes(text.encode("utf-8"), name, kind=kind,
                              metadata=metadata)

    def put_bytes(self, data: bytes, name: str = "artifact.bin", *,
                  kind: str = "artifact",
                  metadata: Mapping[str, Any] | None = None) -> Artifact:
        digest = sha256(data).hexdigest()
        artifact_id = f"{digest[:16]}-{_safe_name(name)}"
        target = (self.artifacts_dir / artifact_id).resolve()
        _ensure_child(self.artifacts_dir, target)
        if not target.exists() or target.read_bytes() != data:
            tmp = target.with_name(f".{target.name}.tmp")
            tmp.write_bytes(data)
            os.replace(tmp, target)
        record = {
            "id": artifact_id,
            "relative_path": str(Path("artifacts") / artifact_id),
            "kind": kind, "sha256": digest, "size_bytes": len(data),
            "metadata": dict(metadata or {}),
        }
        self._manifest[artifact_id] = record
        self._write_manifest()
        return self._from_record(record)

    def get(self, artifact_id: str) -> Artifact | None:
        rec = self._manifest.get(artifact_id)
        return self._from_record(rec) if rec else None

    def list(self, *, kind: str | None = None) -> tuple[Artifact, ...]:
        recs = sorted(self._manifest.values(), key=lambda r: r["id"])
        arts = (self._from_record(r) for r in recs)
        return tuple(a for a in arts if kind is None or a.kind == kind)

    def _load_manifest(self) -> dict[str, dict[str, Any]]:
        if not self.manifest_path.exists():
            return {}
        try:
            raw = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ArtifactStoreError(
                f"invalid manifest: {self.manifest_path}") from exc
        if not isinstance(raw, dict):
            raise ArtifactStoreError("manifest must be a JSON object")
        return raw

    def _write_manifest(self) -> None:
        payload = json.dumps(self._manifest, indent=2, sort_keys=True)
        tmp = self.manifest_path.with_suffix(".json.tmp")
        tmp.write_text(payload + "\n", encoding="utf-8")
        os.replace(tmp, self.manifest_path)

    def _from_record(self, rec: Mapping[str, Any]) -> Artifact:
        path = (self.root / str(rec["relative_path"])).resolve()
        _ensure_child(self.root, path)
        return Artifact(
            id=str(rec["id"]), path=path, kind=str(rec["kind"]),
            sha256=str(rec["sha256"]), size_bytes=int(rec["size_bytes"]),
            metadata=dict(rec.get("metadata") or {}))


def _safe_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(name).name).strip("._-")
    return (cleaned or "artifact.bin")[:96]


def _ensure_child(parent: Path, child: Path) -> None:
    p, c = parent.resolve(), child.resolve()
    if c != p and p not in c.parents:
        raise ArtifactStoreError(f"path escapes store: {child}")
