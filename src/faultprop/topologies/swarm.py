"""Topology 3: peer-to-peer handoffs.

Verified against the Strands docs (2026-08-30):
    from strands.multiagent import Swarm
    swarm = Swarm(agents=[investigator, risk, resolver],
                  entry_point=investigator,      # defaults to agents[0]
                  max_handoffs=20, max_iterations=20,
                  execution_timeout=900.0, node_timeout=300.0,
                  repetitive_handoff_detection_window=0)
    result = swarm(task)          # or: await swarm.invoke_async(task)

Handoffs use an auto-injected `handoff_to_agent(agent_name, message, context)` tool.
`SwarmResult` carries: status, node_history, results (per agent), execution_count,
execution_time, accumulated_usage.

Experiment notes:
- `node_history` is the handoff sequence — a primary containment signal (WP 2.3).
- Set `max_handoffs` / `max_iterations` **explicitly** and record them: fault injection
  is expected to increase handoffs, and hitting a default silently would confound
  "the topology failed" with "the framework capped it".
- `repetitive_handoff_detection_window` must be identical across conditions, or
  ping-pong suppression becomes an uncontrolled variable.

TODO(WP 1.3).
"""
from __future__ import annotations

from typing import Callable

from .base import Topology, register


@register
class Swarm(Topology):
    name = "swarm"

    def run(self, tools: list[Callable], task: str) -> dict:
        raise NotImplementedError("see module docstring")
