"""Typed planning artifacts for the planning ladder (pure dataclasses).

These mirror the Math-To-Manim Pydantic artifacts (math_to_manim/schemas/
artifacts.py) but use only the standard library, so they run with no pydantic
dependency. Each rung of the planning ladder becomes a small typed object you
can serialize to JSON and inspect before writing any Manim code:

    ConceptIntent      rung 0  the single idea, audience, misconceptions
    ConceptNode        rung 1  one node of the prerequisite graph
    KnowledgeGraph     rung 1  the graph, with .curriculum_order() (rung 2)
    Equation/MathPacket rung 3 definitions, key equations, common errors
    StoryboardScene    rung 4  one Act's beat: narration, what moves, camera
    VisualStoryboard   rung 4  the ordered list of Acts
    SceneSpec          rung 5  the per-Act object/animation contract

Use to_dict()/to_json() to hand any rung to the ArtifactStore.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import Any

from .graph import topological_sort


@dataclass
class ConceptIntent:
    primary_concept: str
    target_audience: str | None = None
    learning_objectives: list[str] = field(default_factory=list)
    misconceptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ConceptNode:
    id: str
    label: str
    status: str = "build"  # "build" (teach in video) or "have" (assumed known)
    depends_on: list[str] = field(default_factory=list)
    summary: str | None = None


@dataclass
class KnowledgeGraph:
    """The reverse knowledge tree. Root is the target idea; leaves are
    assumed knowledge. curriculum_order() returns the teaching sequence."""

    nodes: list[ConceptNode] = field(default_factory=list)
    root_id: str | None = None

    def add(self, node: ConceptNode) -> "KnowledgeGraph":
        self.nodes.append(node)
        return self

    def curriculum_order(self, *, build_only: bool = True) -> list[str]:
        """Dependency-first order of node ids (rung 2). Raises GraphCycleError
        on a circular prerequisite, which is a real plan defect."""
        graph = {n.id: list(n.depends_on) for n in self.nodes}
        order = topological_sort(graph)
        if build_only:
            build = {n.id for n in self.nodes if n.status == "build"}
            order = [nid for nid in order if nid in build]
        return order

    def to_dict(self) -> dict[str, Any]:
        return {"root_id": self.root_id,
                "nodes": [asdict(n) for n in self.nodes]}


@dataclass
class Equation:
    latex: str
    description: str | None = None


@dataclass
class MathPacket:
    concept_id: str | None = None
    definitions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    key_equations: list[Equation] = field(default_factory=list)
    common_errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d


@dataclass
class StoryboardScene:
    id: str
    title: str
    narration: str | None = None
    appears_first: str | None = None     # what enters first
    moves: str | None = None             # what animates
    invariant: str | None = None         # what stays anchored
    camera: str | None = None
    concept_ids: list[str] = field(default_factory=list)
    duration_seconds: float | None = None


@dataclass
class VisualStoryboard:
    title: str
    scenes: list[StoryboardScene] = field(default_factory=list)

    def act_table(self) -> str:
        """Render the Act table the user approves in PHASE 1."""
        rows = ["| Act | Title | What it shows |", "|---|---|---|"]
        for i, s in enumerate(self.scenes, 1):
            shows = s.moves or s.narration or ""
            rows.append(f"| Act {i} | {s.title} | {shows} |")
        return "\n".join(rows)

    def to_dict(self) -> dict[str, Any]:
        return {"title": self.title, "scenes": [asdict(s) for s in self.scenes]}


@dataclass
class SceneObject:
    id: str
    type: str                            # e.g. "Axes", "MathTex", "Surface"
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class SceneAnimation:
    action: str                          # e.g. "Create", "Write", "Transform"
    target: str | None = None
    run_time: float | None = None


@dataclass
class SceneSpec:
    """Rung 5: the per-Act contract a code generator turns into Manim."""

    scene_class: str                     # e.g. "Act1_Hook"
    base: str = "Scene"                  # Scene | ThreeDScene | MovingCameraScene
    objects: list[SceneObject] = field(default_factory=list)
    animations: list[SceneAnimation] = field(default_factory=list)
    duration_seconds: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def to_json(obj: Any) -> str:
    """Serialize any artifact (or to_dict-able object) to pretty JSON."""
    if hasattr(obj, "to_dict"):
        obj = obj.to_dict()
    elif hasattr(obj, "__dataclass_fields__"):
        obj = asdict(obj)
    return json.dumps(obj, indent=2, sort_keys=True, default=str)
