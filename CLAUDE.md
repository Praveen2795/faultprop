# faultprop — repo conventions

Research harness for paper 1. Study design and the task breakdown live in a separate private planning repo (not published with this code).

## What it does
Builds one synthetic card-dispute workflow four ways (single / supervisor / swarm / pipeline) in Strands, injects faults at the tool boundary, and measures which topology takes a **confident wrong money-moving action** and how far bad data spreads between agents.

## Commands
```bash
uv sync --extra dev
uv run pytest -q
uv run faultprop cases                       # list dispute cases
uv run faultprop smoke --model <cheap-model> # one episode, single topology, no faults
uv run faultprop grid --topology single --fault stale --lam 0.5 --repeats 5
```

## Invariants — breaking these invalidates the experiment
1. **Identical prompts across all four topologies.** `topologies/prompts.py` is shared. If a prompt changes it changes for every topology, or the comparison is meaningless.
2. **Never fault `execute_action`.** We measure wrong *decisions*, not a broken recorder. Enforced in `chaos/faults.py`.
3. **All data synthetic.** No real customers, no employer data, ever.
4. **Deterministic scoring wherever possible.** LLM judging is only for containment, and must be validated against 100 hand-checks with an agreement rate reported.
5. **Freeze `docs/hypotheses.md` before the full grid run.** Do not edit hypotheses after seeing results.
6. Every episode is reproducible from its JSONL trace + seed. Seeds are derived, not random.

## Layout
`workflow/` job + 6 mocked tools + case loader · `chaos/` fault injection · `topologies/` the four shapes + shared prompts · `metrics/` scoring · `runner.py` grid → JSONL in `runs/` · `cases/` YAML cases · `docs/` hypotheses, decisions, MAST mapping.

## Docs
An MCP server for the Strands documentation is configured in `.mcp.json` (`strands-agents`, via `uvx strands-agents-mcp-server`; tools `search_docs`, `fetch_doc`). **Use it instead of assuming API shapes.** If it shows as pending approval, run `claude` and approve it. Fallback: https://strandsagents.com/docs/

## Status
Skeleton complete and tested. `single` topology wired; **supervisor / swarm / pipeline are stubs** (see their module docstrings for the intended Strands pattern). Tracing hook in `tracing.py` is minimal — capturing inter-agent messages is WP 1.5 and is the hardest remaining piece.

Contributors: see `CONTRIBUTING.md` (peer onboarding, case-writing brief).
