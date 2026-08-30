# Contributing (for co-authors)

Welcome. Read the design page Praveen shared with you first — it explains the whole study in plain language, with diagrams.

## Setup
```bash
uv sync --extra dev
uv run pytest -q          # should pass
uv run faultprop cases    # lists the dispute cases
```

## WP 1.1 — Writing cases (the first delegated job)
Goal: 24 cases in `cases/`, roughly 6 per action, 3–4 marked `ambiguous: true`.

1. Copy `cases/_TEMPLATE.yaml` to `cases/NNN-short-name.yaml` (NNN = next number).
2. Invent a realistic dispute. **All data synthetic** — invented names, merchants, amounts. Never copy from a real case.
3. Fill every field. `correct_action` must be defensible from the data alone; write the reason in `rationale` (1–2 sentences).
4. Mix it up: card-present vs online vs recurring; long-tenure vs new customers; high vs low fraud scores; some where facts conflict (→ `ESCALATE_TO_HUMAN`), some where a document would settle it (→ `REQUEST_DOCUMENTS`).
5. Run `uv run faultprop cases` — your case must load without errors.
6. Open a PR. Praveen reviews for (a) is the correct action really unambiguous, (b) is it distinct from existing cases.

Definition of done: 24 cases load; action counts are balanced; each rationale would convince a bank analyst.

## Ground rules
- Nothing from any employer. Nothing real. If in doubt, invent it.
- Don't change prompts in `topologies/prompts.py` without discussing — they must stay identical across topologies.
- Log decisions in `docs/decisions.md`.
