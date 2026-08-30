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
    If either H0 fails, faulted results must be interpreted with caution and the discrepancy reported.
H1  Under injected faults the *gap* between structured (pipeline, supervisor) and unstructured (single, swarm)
    topologies widens: structure buys more safety when tools are unreliable than when they are reliable.
H2  Swarm shows the worst containment: corrupted or injected values reach a second agent more often than in
    supervisor or pipeline.
H3  Quiet faults (WRONG_PLAUSIBLE, STALE) produce more silent wrong actions than loud faults
    (TIMEOUT, RATE_LIMIT), because loud failures trigger escalation and quiet ones do not.
H4  `fault_response = proceeded` is the dominant mechanism behind silent wrong actions, across topologies.
H5  Safety costs tokens: topologies with fewer silent failures consume more tokens under faults.
H6  Fault tolerance improves less with a stronger model than task accuracy does (echoing ToolMaze).

Analysis plan: per hypothesis, the exact comparison and statistic (write before running).
- H0a/H1: silent_wrong rate per topology × λ, 95% Wilson CIs; H1 tested as a topology×λ interaction.
- H0b: recovery rate (safe_failure ∪ success after a fault) supervisor vs pipeline, Fisher exact.
- H2: contained rate per multi-agent topology, Fisher exact pairwise.
- H3: silent_wrong by fault class, quiet vs loud grouped, chi-squared.
- H4: distribution of fault_response conditioned on silent_wrong.
- H5: tokens vs silent_wrong per topology (Pareto plot), Spearman.
- H6: Δ(success) vs Δ(silent_wrong) between cheap and frontier model.
