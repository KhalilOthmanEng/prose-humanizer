"""Graph normalization and deterministic topological sorting.

Ported from Math-To-Manim (math_to_manim/tools/graph.py), pure standard
library. This is the engine behind the planning ladder's curriculum order:
feed it the prerequisite graph (each concept plus the concepts it depends on)
and it returns the concepts in dependency-first teaching order, which becomes
the Act sequence. Ties break lexicographically so repeated runs are identical.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import heapq
from typing import Any


class GraphError(ValueError):
    """Base error for invalid graph inputs."""


class GraphCycleError(GraphError):
    """Raised when a graph contains a dependency cycle.

    A cycle in the prerequisite graph means concept A needs B which needs A.
    That is a planning defect: the curriculum cannot be ordered. Surface it to
    the user rather than emitting an arbitrary order.
    """

    def __init__(self, nodes: Iterable[str]) -> None:
        self.nodes = tuple(sorted(nodes))
        super().__init__(
            "Graph contains a dependency cycle involving: "
            + ", ".join(self.nodes)
        )


@dataclass(frozen=True)
class GraphNode:
    """A lightweight node spec accepted by normalize_graph."""

    id: str
    dependencies: tuple[str, ...] = ()


NormalizedGraph = dict[str, tuple[str, ...]]


def normalize_graph(
    graph: Mapping[str, Iterable[str] | str | None] | Iterable[Any],
) -> NormalizedGraph:
    """Return a canonical adjacency mapping of node to sorted dependencies.

    Accepts a mapping, GraphNode objects, dicts with 'id' and
    'dependencies'/'depends_on', plain strings, or objects with matching
    attributes. Missing dependency nodes are added with no dependencies so the
    result is closed over every referenced id.
    """

    normalized: dict[str, set[str]] = {}
    for node_id, dependencies in _iter_node_specs(graph):
        canonical_id = _coerce_node_id(node_id)
        deps = {_coerce_node_id(dep) for dep in _coerce_dependencies(dependencies)}
        normalized.setdefault(canonical_id, set()).update(deps)
        for dep in deps:
            normalized.setdefault(dep, set())
    return {nid: tuple(sorted(deps)) for nid, deps in sorted(normalized.items())}


def topological_sort(
    graph: Mapping[str, Iterable[str] | str | None] | Iterable[Any],
) -> list[str]:
    """Return node ids in deterministic dependency-first order (Kahn's algo)."""

    normalized = normalize_graph(graph)
    dependents: dict[str, set[str]] = defaultdict(set)
    indegree: dict[str, int] = {}
    for node_id, dependencies in normalized.items():
        indegree[node_id] = len(dependencies)
        for dep in dependencies:
            dependents[dep].add(node_id)

    ready = [nid for nid, deg in indegree.items() if deg == 0]
    heapq.heapify(ready)
    ordered: list[str] = []
    while ready:
        node_id = heapq.heappop(ready)
        ordered.append(node_id)
        for dependent in sorted(dependents.get(node_id, ())):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, dependent)

    if len(ordered) != len(normalized):
        remaining = [nid for nid, deg in indegree.items() if deg > 0]
        raise GraphCycleError(remaining)
    return ordered


def _iter_node_specs(graph: Any) -> Iterable[tuple[Any, Any]]:
    if isinstance(graph, Mapping):
        yield from graph.items()
        return
    for node in graph:
        if isinstance(node, str):
            yield node, ()
        elif isinstance(node, GraphNode):
            yield node.id, node.dependencies
        elif isinstance(node, Mapping):
            if "id" not in node:
                raise GraphError("Graph node dicts must include an 'id' key")
            yield node["id"], node.get("dependencies", node.get("depends_on", ()))
        else:
            node_id = getattr(node, "id", None)
            if node_id is None:
                raise GraphError(f"Unsupported graph node type: {type(node).__name__}")
            deps = getattr(node, "dependencies", getattr(node, "depends_on", ()))
            yield node_id, deps


def _coerce_node_id(value: Any) -> str:
    if not isinstance(value, str):
        raise GraphError(f"Graph node ids must be strings, got {type(value).__name__}")
    node_id = value.strip()
    if not node_id:
        raise GraphError("Graph node ids must not be empty")
    return node_id


def _coerce_dependencies(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    try:
        return tuple(value)
    except TypeError as exc:
        raise GraphError("Dependencies must be an iterable of node ids") from exc
