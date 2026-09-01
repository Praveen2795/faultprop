# faultprop — Fail Safe or Fail Silent?
**Fault propagation across multi-agent topologies in a synthetic financial-service workflow.**

Research harness for paper 1 of the "reliable agents in regulated finance" program.
Design doc: kept in a separate private planning repo; the study is summarised below and in `CLAUDE.md`.

## What this does, in one paragraph
A fake card-dispute triage workflow (six mocked tools, ~24 hand-written cases with known correct answers) is built four ways in Strands — single agent, supervisor+workers, swarm, fixed pipeline — with identical prompts. A "chaos" layer breaks the tools on purpose (timeouts, stale data, plausible-but-wrong values, injected instructions...). We run every combination many times and count how often each design **quietly does the wrong thing**, how far bad data spreads between agents, and what it costs.

## Layout
```
src/faultprop/
  workflow/    the dispute-triage job: data models, six mocked tools, ground-truth loader
  chaos/       the fault-injection layer wrapped around tools
  topologies/  the four agent shapes (same prompts, different wiring)
  metrics/     scoring one run: success, silent-wrong-action, containment, cost, MAST label
  runner.py    experiment grid → JSONL traces in runs/
cases/         hand-written dispute cases (YAML), one file each
runs/          output traces (gitignored except samples)
notebooks/     analysis + figures
paper/         LaTeX for the workshop paper
docs/          design notes, decisions log
tests/         unit tests for tools, chaos, metrics
```

## Quick start
```bash
uv sync                          # creates .venv with deps
cp .env.example .env             # add API keys
uv run faultprop smoke           # 1 case × 1 topology × no faults, on a free/cheap model
uv run faultprop grid --topology single --fault none --repeats 1
```

## Status — work packages
Owner: **P** Praveen · **Peer** delegable · 🔴 weekend deep block · 🟢 weeknight chunk

**Phase 0 · Setup (Sep 1–7)**
- [x] 0.1 ✅ P — `.env` + `faultprop smoke` passes (local `ollama:gemma4:e2b`, 2026-08-30)
- [ ] 0.2 🟢 P — arXiv account; endorsement status known; endorsers listed
- [ ] 0.6 🟢 P — **model bake-off**: run both cases on the 2 verified candidates via OpenRouter, pick the **workhorse**
      candidates: `deepseek/deepseek-v4-flash-0731` ($11 full grid) · `z-ai/glm-5.3-flash` ($14 full grid)
      whichever loses becomes the family control; its own family's Pro tier becomes the tier control
      `uv run faultprop grid --topology single --fault none --model openrouter:<id> --repeats 3`
      compare: correct action, tool_calls, evidence_complete, tokens, latency. Cheapest *reliable* wins —
      **and it must have a stronger sibling in the same family** (needed as the tier control, see DESIGN §5a).
- [ ] 0.6b 🟢 P — *fallback only, if both candidates miss the ≥80% bar*: direct OpenAI key, GPT-5 Nano → Mini → 5 ladder
- [ ] 0.3 🟢 P — peers onboarded (`CONTRIBUTING.md`, repo access)
- [ ] 0.4 🟢 P — ACM/AAAI membership; Zenodo account
- [ ] 0.5 🟢 **Peer** — scoop watch: fortnightly arXiv search, log hits (starts Sep, runs to publication)

**Phase 1 · Build (Sep 8 – Oct 5)**
- [ ] 1.0 🟢 P — read the six closest neighbours; two-page positioning note (four-axis intersection)
- [ ] 1.1 🟢 **Peer** — 24 cases in `cases/` (2/24 done)
- [ ] 1.2 🔴 P — supervisor topology
- [ ] 1.3 🔴 P — swarm topology
- [ ] 1.4 🔴 P — pipeline topology
- [ ] 1.5 🔴 P — tracing hook (inter-agent messages + tool calls with agent id)
- [ ] 1.6 🟢 Peer — hand-score 20 traces vs `score_episode`
- [ ] 1.7 🟢 P+Peer — tests for topologies + tracing
- [ ] 1.8 🔴 P — 50-episode smoke, all 4 topologies
- [ ] 1.8b 🟢 P — classify fault recoverability (does each fault have a recovery path?)
- [ ] 1.9 🟢 P — **freeze `docs/hypotheses.md` + analysis plan**
- [ ] **G1 — Oct 5 gate**

**Phase 2 · Run (Oct 6 – Nov 9)**
- [ ] 2.1 🔴 P / 🟢 Peer — full grid, workhorse model (~8,640 episodes)
- [ ] 2.2 🔴 P — reduced grids, model #2 + frontier
- [ ] 2.3 🔴 P — containment judge
- [ ] 2.4 🟢 **Peer** — hand-check 100 judgments, Cohen's κ
- [ ] 2.5 🟢 Peer — MAST labels (`docs/mast-mapping.md`)
- [ ] 2.6 🔴 P — analysis notebook (CIs, tests, effect sizes, cost)
- [ ] 2.7 🟢 P+Peer — figures

**Phase 3 · Write & release (Nov 10 – Dec 19)**
- [ ] 3.1 🟢 Peer draft — Related Work
- [ ] 3.2 🟢 P — Method
- [ ] 3.3 🔴 P — Results, Discussion, validator table
- [ ] 3.4 🟢 P — Intro, Abstract, Limitations
- [ ] 3.5 🟢 Peer — cold read
- [ ] 3.6 🟢 P+Peer — public-release cleanup (README, LICENSE, samples, reproduce script)
- [ ] 3.7 🟢 Peer draft — blog post
- [ ] **3.8a 🟢 P — Nov 7 early-preprint decision: short arXiv if H0a/H0b replicate + one strong faulted result**
- [ ] **3.8 🟢 P — full arXiv + public GitHub + Zenodo DOI + blog (Dec 8–19)**
- [ ] 3.9 🟢 Peer — announcements

**Phase 4 · Submit & profile (Dec – Feb 2027)**
- [ ] 4.1 AAAI-27 workshop (Nov 20) — only if remote presentation allowed; decide Oct 2
- [ ] 4.2 ICLR 2027 workshop submission (≈ early Feb ⚠ verify)
- [ ] 4.3 reviewer sign-ups · 4.4 one talk · 4.5 Strands PRs · 4.6 letter groundwork · 4.7 RFI watch · 4.8 attorney consult

## Principles
1. **No real data, no employer data, ever.** Everything here is synthetic.
2. **Same prompts across topologies.** If a prompt changes, it changes for all four.
3. **Deterministic scoring wherever possible.** LLM judge only for containment, with hand checks.
4. **Freeze hypotheses before the full run.** See docs/hypotheses.md.
5. **Every run is reproducible** from its JSONL trace + config hash.

License: MIT (to be added at release).
