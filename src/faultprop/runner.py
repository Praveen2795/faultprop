"""Run an experiment grid and write one JSONL line per episode to runs/."""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from .chaos import Fault, FaultConfig, wrap_tools
from .metrics import score_episode
from .topologies import TOPOLOGIES
from .workflow import tools as wf_tools
from .workflow.cases import load_cases

# Ensure topologies register themselves.
from .topologies import single, supervisor, swarm, pipeline  # noqa: F401,E402

RUNS_DIR = Path(__file__).resolve().parents[2] / "runs"


def task_text(case) -> str:
    return (f"Handle dispute {case.dispute.dispute_id} for customer {case.customer.customer_id} "
            f"about transaction {case.dispute.txn_id}. Decide exactly one action.")


def run_grid(topology: str, fault: str, lam: float, model: str, repeats: int = 1,
             cases: list[str] | None = None, out: Path | None = None) -> Path:
    topo_cls = TOPOLOGIES[topology]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out or RUNS_DIR / f"{stamp}_{topology}_{fault}_{lam}_{model.replace('/', '-')}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("a") as f:
        for case in load_cases(cases):
            for rep in range(repeats):
                seed = int(hashlib.sha256(f"{case.case_id}:{rep}:{fault}:{lam}".encode()).hexdigest(), 16) % 2**31
                cfg = FaultConfig(fault=Fault(fault), lam=lam, seed=seed)
                wf_tools.set_case(case)
                tools = wrap_tools(wf_tools.ALL_TOOLS, cfg)
                topo = topo_cls(model=model)
                t0 = time.time()
                error = None
                try:
                    trace = topo.run(tools, task_text(case))
                except Exception as e:  # the episode itself may blow up — that is data
                    trace = {"final_action": None, "messages": [], "tool_calls": [], "n_actions": 0}
                    error = repr(e)
                trace["wall_s"] = time.time() - t0
                rec = {
                    "ts": stamp, "topology": topology, "fault": fault, "lam": lam, "model": model,
                    "case_id": case.case_id, "rep": rep, "seed": seed, "error": error,
                    "faults_injected": cfg.log,
                    "score": score_episode(case, trace, cfg.log, cfg.calls),
                    "calls": cfg.calls,
                    "trace": trace,
                }
                f.write(json.dumps(rec, default=str) + "\n")
    return out
