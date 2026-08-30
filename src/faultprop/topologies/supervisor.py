"""Topology 2: supervisor delegates to Investigator, Risk and Resolver.

Verified against the Strands docs (agents-as-tools, 2026-08-30): specialist Agent
instances are passed **directly** in the orchestrator's `tools` list — the SDK converts
each one into a tool taking an `input` string. No manual @tool wrapping is needed.

TODO(WP 1.2):
    investigator = Agent(model=m, system_prompt=INVESTIGATOR, name="investigator",
                         tools=[get_customer, get_transactions, get_dispute])
    risk         = Agent(model=m, system_prompt=RISK, name="risk",
                         tools=[fraud_score, kyc_status])
    resolver     = Agent(model=m, system_prompt=RESOLVER, name="resolver",
                         tools=[execute_action])
    supervisor   = Agent(model=m, system_prompt=SUPERVISOR,
                         tools=[investigator, risk, resolver], callback_handler=None)
Tools arrive here already chaos-wrapped and @tool-decorated; split them by name.
Only the resolver gets execute_action, so "who can move money" differs by topology.
"""
from __future__ import annotations

from typing import Callable

from .base import Topology, register


@register
class Supervisor(Topology):
    name = "supervisor"

    def run(self, tools: list[Callable], task: str) -> dict:
        raise NotImplementedError("see module docstring")
