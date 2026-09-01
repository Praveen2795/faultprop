# Pre-registered hypotheses (FREEZE before the full grid; do not edit after)
Frozen on: ____ (fill in date)

Vocabulary: fault classes map to ToolBench-X hazards (see DESIGN.md §3c); "silent failure" per Advani
(2606.09863); "abstention" / "post-hoc abstention" per AgentAbstain (2607.10059).

Anchor: Kim et al., *Towards a Science of Scaling Agent Systems* (arXiv 2512.08296) found, with tools held
reliable, that centralized coordination contains error propagation better than decentralized
(trace-level amplification 4.4× vs 17.2×). Our λ=0 condition is a replication of that ordering; every other
condition asks whether it survives when tools fail.

H0a (replication, no faults) At λ=0, silent-wrong rates order supervisor ≤ pipeline < single < swarm,
    consistent with Kim et al.'s centralized-beats-decentralized result.
H0b (replication, under faults) Closed-loop/orchestrated designs (supervisor) recover from injected faults
    more often than the linear pipeline, consistent with MAS-FIRE (arXiv 2602.19843) — tested here with
    tool-boundary faults rather than their agent/message faults.
    If either H0a or H0b fails, faulted results must be interpreted with caution and the discrepancy
    reported prominently rather than buried.
H1  Under injected faults the *gap* between structured (pipeline, supervisor) and unstructured (single, swarm)
    topologies widens: structure buys more safety when tools are unreliable than when they are reliable.
H2  Swarm shows the worst containment: corrupted or injected values reach a second agent more often than in
    supervisor or pipeline.
H3  Quiet faults (WRONG_PLAUSIBLE, STALE) produce more silent wrong actions than loud faults
    (TIMEOUT, RATE_LIMIT), because loud failures trigger escalation and quiet ones do not.
H4  Among silent-wrong episodes, `fault_response = "proceeded"` (money moved with NO retry of
    the faulted tool) outnumbers `"retried_then_proceeded"` — i.e. agents mostly fail to react
    to a fault at all, rather than reacting and still getting it wrong.
    ⚠️ Restated 2026-08-31. The original wording was unfalsifiable: `fault_response` was
    computed as `final in MONEY_MOVING`, and `silent_wrong` also requires `final in
    MONEY_MOVING`, so "proceeded" was guaranteed at 100% in every topology. The retry split
    makes it testable. A stronger version — did the agent *notice* the fault — needs the
    message trace from WP 1.5 and stays out of scope until then.
H5  Safety costs tokens: topologies with fewer silent failures consume more tokens under faults.
H6  Fault tolerance improves less with a stronger model than task accuracy does (echoing ToolMaze).
    Scope: tested on ONE same-family pair (workhorse vs tier control) — a directional check, not a
    scaling law. Phrase any claim as "in our setup"; see DESIGN.md §5a "Limits of this design".

Analysis plan: per hypothesis, the exact comparison and statistic (write before running).
- H0a/H1: silent_wrong rate per topology × λ, 95% Wilson CIs; H1 tested as a topology×λ interaction.
- H0b: recovery rate (safe_failure ∪ success after a fault) supervisor vs pipeline, Fisher exact.
- H2: contained rate per multi-agent topology, Fisher exact pairwise.
- H3: silent_wrong by fault class, quiet vs loud grouped, chi-squared.
- H4: distribution of fault_response conditioned on silent_wrong, chi-squared over {proceeded, retried_then_proceeded, escalated, abandoned}. Episodes labelled `fault_after_decision` are excluded — the fault landed after execute_action, so the agent had no opportunity to respond.
- H5: tokens vs silent_wrong per topology (Pareto plot), Spearman.
- H6: Δ(success) vs Δ(silent_wrong) between workhorse and same-family tier control (reduced grid; wide CIs expected — directional only).
