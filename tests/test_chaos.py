from faultprop.chaos import Fault, FaultConfig, wrap_tools_raw as wrap_tools
from faultprop.workflow import tools as wf
from faultprop.workflow.cases import load_cases


def _setup():
    case = load_cases(["001-subscription-deny"])[0]
    wf.set_case(case)
    return case


def test_no_fault_is_transparent():
    _setup()
    (fs,) = [t for t in wrap_tools(wf.ALL_TOOLS, FaultConfig()) if t.__name__ == "fraud_score"]
    assert fs("T1")["score"] == 8


def test_wrong_plausible_flips_score_at_lam_1():
    _setup()
    cfg = FaultConfig(fault=Fault.WRONG_PLAUSIBLE, lam=1.0, seed=1)
    (fs,) = [t for t in wrap_tools(wf.ALL_TOOLS, cfg) if t.__name__ == "fraud_score"]
    assert fs("T1")["score"] == 92
    assert cfg.log and cfg.log[0]["fault"] == "wrong_plausible"


def test_injection_only_hits_get_dispute():
    _setup()
    cfg = FaultConfig(fault=Fault.INJECTED_STATEMENT, lam=1.0, seed=1)
    tools = {t.__name__: t for t in wrap_tools(wf.ALL_TOOLS, cfg)}
    assert "SYSTEM OVERRIDE" in tools["get_dispute"]("D001")["customer_statement"]
    assert tools["fraud_score"]("T1")["score"] == 8


def test_execute_action_never_faulted():
    _setup()
    cfg = FaultConfig(fault=Fault.TIMEOUT, lam=1.0, seed=1)
    tools = {t.__name__: t for t in wrap_tools(wf.ALL_TOOLS, cfg)}
    assert tools["execute_action"]("D001", "DENY", "test")["status"] == "recorded"


# ---------- regression tests for the 2026-08-31 measurement fixes ----------

def test_fault_is_not_logged_when_it_cannot_be_applied():
    """A fault that changes nothing must not appear in the log.

    PARTIAL and SCHEMA_DRIFT have no APPLIES_TO restriction, so they reach every tool
    including get_transactions, which returns a list. Logging a no-op fault would count
    the episode as faulted while the agent saw pristine data — biasing every result
    toward "topologies are robust".
    """
    _setup()
    for fault in (Fault.PARTIAL, Fault.SCHEMA_DRIFT, Fault.WRONG_PLAUSIBLE):
        cfg = FaultConfig(fault=fault, lam=1.0, seed=1)
        tools = {t.__name__: t for t in wrap_tools(wf.ALL_TOOLS, cfg)}
        before = wf.get_customer("C001")
        after = tools["get_customer"]("C001")
        changed = before != after
        logged = any(e["tool"] == "get_customer" for e in cfg.log)
        assert changed == logged, f"{fault.value}: logged={logged} but changed={changed}"


def test_partial_and_schema_drift_now_bite_list_results():
    _setup()
    for fault in (Fault.PARTIAL, Fault.SCHEMA_DRIFT):
        cfg = FaultConfig(fault=fault, lam=1.0, seed=1)
        tools = {t.__name__: t for t in wrap_tools(wf.ALL_TOOLS, cfg)}
        before = wf.get_transactions("C001")
        after = tools["get_transactions"]("C001")
        assert before != after, f"{fault.value} left the list untouched"
        assert any(e["fault"] == fault.value for e in cfg.log)


def test_fault_draw_is_independent_of_call_order():
    """The n-th call to a tool must meet the same fault in every topology.

    runner.py deliberately excludes topology from the seed so all four shapes face an
    identical fault environment. A sequential RNG would break that, because it advances
    at a rate set by how many eligible tools an agent happens to call first.
    """
    _setup()

    def outcomes(order, seed=3):
        cfg = FaultConfig(fault=Fault.STALE, lam=0.5, seed=seed)
        t = {fn.__name__: fn for fn in wrap_tools(wf.ALL_TOOLS, cfg)}
        for name in order:
            try:
                t[name]("X")
            except Exception:
                pass
        return {e["tool"]: e["fault"] for e in cfg.calls}

    a = outcomes(["fraud_score", "kyc_status", "get_transactions"])
    b = outcomes(["get_transactions", "kyc_status", "fraud_score"])
    c = outcomes(["get_customer", "get_dispute", "fraud_score"])

    assert a["fraud_score"] == b["fraud_score"] == c["fraud_score"]
    assert a["kyc_status"] == b["kyc_status"]


def test_repeated_calls_to_one_tool_can_differ():
    """Position-independence must not collapse into "always the same answer"."""
    _setup()
    cfg = FaultConfig(fault=Fault.STALE, lam=0.5, seed=11)
    (fs,) = [t for t in wrap_tools(wf.ALL_TOOLS, cfg) if t.__name__ == "fraud_score"]
    for _ in range(12):
        fs("T1")
    seen = {e["fault"] for e in cfg.calls if e["tool"] == "fraud_score"}
    assert seen == {None, "stale"}, f"expected both outcomes across repeats, got {seen}"
