"""Topology 1: one ReAct agent does everything."""
from __future__ import annotations

import time
from typing import Callable

from strands import Agent

from ..modelspec import resolve
from ..tracing import capture
from .base import Topology, register
from .prompts import SINGLE


@register
class SingleAgent(Topology):
    name = "single"

    def run(self, tools: list[Callable], task: str) -> dict:
        t0 = time.time()
        with capture() as trace:
            agent = Agent(
                model=resolve(self.model),
                system_prompt=SINGLE,
                tools=tools,
                callback_handler=None,
            )
            result = agent(task)
        trace["latency_s"] = time.time() - t0
        trace["usage"] = _usage(result)
        trace["stop_reason"] = getattr(result, "stop_reason", None)
        return trace


def _usage(result) -> dict:
    """Token usage, tolerant of provider differences."""
    metrics = getattr(result, "metrics", None)
    usage = getattr(metrics, "accumulated_usage", None) if metrics else None
    if usage is None:
        return {}
    return dict(usage) if not isinstance(usage, dict) else usage
