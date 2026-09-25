"""m2m_tools: the runnable deterministic tool layer for the
3b1b-scientific-explanation skill.

Adapted from the Math-To-Manim (M2M2) repository's deterministic tools and
rendering wrappers (the LLM/agent/CLI/provider infrastructure was intentionally
left out, since it cannot run inside a chat-loaded skill). Everything here is
pure standard library: no pydantic, no Manim install required to run the tools
themselves (Manim/FFmpeg are only invoked by the render helpers, which skip
gracefully when the binaries are absent).

What each module gives the skill:

    graph            deterministic topological sort -> planning ladder rung 2
                     (curriculum order from the prerequisite graph)
    schemas          typed dataclass artifacts for every planning ladder rung
    ast_validation   security + Manim PART I anti-pattern linter (no execution)
    scene_discovery  find Scene classes / render names without importing
    render_commands  build/run manim render, ffmpeg concat, ffprobe sanity
    artifact_store   write inspectable run-bundle JSON (typed-artifacts-first)
    gate             the runnable §7.4 static gate (validate + discover)
    planning         build a curriculum order and an inspectable run bundle

Quickest concrete use, the static gate before a render:

    python -m m2m_tools.gate generated_scene.py --quality h

Programmatic:

    from m2m_tools.ast_validation import validate_scene_source
    from m2m_tools.scene_discovery import scene_names_in_order
    res = validate_scene_source(open("scene.py").read())
    if res.ok:
        names = scene_names_in_order(open("scene.py").read())
"""

from __future__ import annotations

from .ast_validation import (
    PythonAstPolicy,
    ValidationIssue,
    ValidationResult,
    validate_scene_source,
)
from .graph import GraphCycleError, GraphError, normalize_graph, topological_sort
from .render_commands import (
    ToolResult,
    build_manim_command,
    concat_videos,
    probe_video,
    render_manim_scene,
    write_concat_listfile,
)
from .scene_discovery import (
    SceneClass,
    discover_scene_classes,
    discover_scene_classes_in_file,
    scene_names_in_order,
)
from .schemas import (
    ConceptIntent,
    ConceptNode,
    Equation,
    KnowledgeGraph,
    MathPacket,
    SceneSpec,
    StoryboardScene,
    VisualStoryboard,
    to_json,
)

__all__ = [
    "PythonAstPolicy", "ValidationIssue", "ValidationResult",
    "validate_scene_source",
    "GraphCycleError", "GraphError", "normalize_graph", "topological_sort",
    "ToolResult", "build_manim_command", "concat_videos", "probe_video",
    "render_manim_scene", "write_concat_listfile",
    "SceneClass", "discover_scene_classes", "discover_scene_classes_in_file",
    "scene_names_in_order",
    "ConceptIntent", "ConceptNode", "Equation", "KnowledgeGraph", "MathPacket",
    "SceneSpec", "StoryboardScene", "VisualStoryboard", "to_json",
]
