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
