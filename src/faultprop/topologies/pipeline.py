"""Topology 4: fixed DAG Investigator -> Risk -> Resolver, no loops.

Verified against the Strands docs (2026-08-30):
    from strands.multiagent import GraphBuilder
    b = GraphBuilder()
    b.add_node(investigator, "investigator")
    b.add_node(risk, "risk")
    b.add_node(resolver, "resolver")
    b.add_edge("investigator", "risk")
    b.add_edge("risk", "resolver")
    b.set_entry_point("investigator")
    graph = b.build()
    result = graph(task)

`GraphResult` carries: status, execution_order, results (node_id -> NodeResult),
total/completed/failed_nodes, execution_time, accumulated_usage.

Experiment notes:
- `execution_order` shows how far the case got before a fault stopped it — the
  cleanest containment measure of the four topologies.
- No edges back, so a fault cannot cause a retry loop here. That asymmetry versus
  swarm is part of what H1/H2 predict; state it explicitly in the paper.
- ⚠️ Docs give graph timeouts in ms and Swarm timeouts in seconds. Verify empirically
  before the full grid and record the units used.

TODO(WP 1.4).
"""
from __future__ import annotations

from typing import Callable

from .base import Topology, register


@register
class Pipeline(Topology):
    name = "pipeline"

    def run(self, tools: list[Callable], task: str) -> dict:
        raise NotImplementedError("see module docstring")
