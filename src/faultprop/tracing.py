"""Trace capture.

Currently minimal: the action log plus the chaos layer's own fault log. That is enough
for the single-agent topology and for every metric except containment.

WP 1.5 — the documented approach (verified against the Strands docs, 2026-08-30):
Strands integrates natively with **OpenTelemetry** and emits agent, cycle, LLM and tool
spans automatically. Do NOT hand-roll message interception. Instead:

    from strands.telemetry import StrandsTelemetry
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

    exporter = InMemorySpanExporter()
    telemetry = StrandsTelemetry()
    telemetry.tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
    # ... run the episode ...
    spans = exporter.get_finished_spans()   # tool spans carry name, params, results

Per-episode isolation matters: clear the exporter between episodes, or set
`trace_attributes={"episode.id": ...}` on each Agent and filter by it, so traces from
one run never leak into another's containment score.

Multi-agent results also expose structure directly and should be recorded alongside
the spans: `SwarmResult.node_history` (handoff sequence) and
`GraphResult.execution_order` (how far the DAG got).
"""
from __future__ import annotations

from contextlib import contextmanager

from .workflow import tools as wf_tools


@contextmanager
def capture():
    trace: dict = {"messages": [], "tool_calls": [], "final_action": None}
    try:
        yield trace
    finally:
        log = wf_tools.action_log()
        trace["action_log"] = log
        trace["final_action"] = log[0]["action"] if log else None   # first call is binding
        trace["n_actions"] = len(log)
