"""Planning-ladder helpers: turn a prerequisite graph into a curriculum order
and (optionally) write the whole plan as an inspectable run bundle.

This wires graph + schemas + artifact_store together so the planning ladder in
SKILL.md is not just prose. Build the knowledge graph, get the Act order, then
persist every rung as JSON for review before any code is written.

    from m2m_tools.planning import order_curriculum, write_plan_bundle
    from m2m_tools.schemas import ConceptIntent, ConceptNode, KnowledgeGraph

    kg = KnowledgeGraph(root_id="pushover")
    kg.add(ConceptNode("pushover", "Pushover curve",
                       depends_on=["capacity", "demand"]))
    kg.add(ConceptNode("capacity", "Capacity (base shear vs drift)",
                       depends_on=["plastic_hinge"]))
    kg.add(ConceptNode("plastic_hinge", "Plastic hinge", status="have"))
    kg.add(ConceptNode("demand", "Seismic demand", status="have"))

    order = order_curriculum(kg)          # -> ['capacity', 'pushover']
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .artifact_store import ArtifactStore
from .schemas import (
    ConceptIntent,
    KnowledgeGraph,
    MathPacket,
    VisualStoryboard,
    to_json,
)


def order_curriculum(graph: KnowledgeGraph, *, build_only: bool = True) -> list[str]:
    """Return the dependency-first teaching order of the build concepts.

    This ordering is the Act sequence. Raises GraphCycleError if the
    prerequisites are circular, which means the plan itself is broken.
    """

    return graph.curriculum_order(build_only=build_only)


def write_plan_bundle(
    root: str | Path,
    *,
    intent: ConceptIntent | None = None,
    graph: KnowledgeGraph | None = None,
    math_packets: Iterable[MathPacket] = (),
    storyboard: VisualStoryboard | None = None,
) -> ArtifactStore:
    """Persist each provided planning rung as JSON under a run directory.

    Returns the ArtifactStore so the caller can list() what was written. Only
    the rungs you pass are written, so partial plans are fine.
    """

    store = ArtifactStore(root)
    if intent is not None:
        store.put_json(intent.to_dict(), "intent.json", kind="intent")
    if graph is not None:
        payload = graph.to_dict()
        payload["curriculum_order"] = graph.curriculum_order()
        store.put_json(payload, "knowledge_graph.json", kind="graph")
    for i, packet in enumerate(math_packets):
        store.put_text(to_json(packet), f"math_packet_{i}.json", kind="math")
    if storyboard is not None:
        store.put_json(storyboard.to_dict(), "storyboard.json", kind="storyboard")
        store.put_text(storyboard.act_table(), "act_table.md", kind="storyboard")
    return store
