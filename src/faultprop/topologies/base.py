"""Topology interface. Each topology takes chaos-wrapped tools and returns a trace.

A trace is a plain dict:
  {
    "final_action": "REFUND" | ... | None,
    "messages": [ {agent, role, content} ... ],   # every inter-agent message, for containment
    "tool_calls": [ {agent, tool, args, result_or_error} ... ],
    "usage": {"input_tokens": int, "output_tokens": int},
    "latency_s": float,
  }
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


class Topology(ABC):
    name: str = "base"

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def run(self, tools: list[Callable], task: str) -> dict:
        ...


TOPOLOGIES: dict[str, type[Topology]] = {}


def register(cls: type[Topology]) -> type[Topology]:
    TOPOLOGIES[cls.name] = cls
    return cls
