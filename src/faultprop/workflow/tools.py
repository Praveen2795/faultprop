"""The six mocked tools. Each is a plain function over the current Case.

They are wrapped by the chaos layer (faultprop.chaos) before being handed to agents,
so this file knows nothing about faults. Keep it boring on purpose.
"""
from __future__ import annotations

from .models import Action, Case

# The "current case" is set by the runner before each episode.
_CURRENT: Case | None = None
_ACTION_LOG: list[dict] = []


def set_case(case: Case) -> None:
    global _CURRENT, _ACTION_LOG
    _CURRENT = case
    _ACTION_LOG = []


def action_log() -> list[dict]:
    return list(_ACTION_LOG)


def _case() -> Case:
    assert _CURRENT is not None, "set_case() must be called before tools are used"
    return _CURRENT


def get_customer(customer_id: str) -> dict:
    """Return the customer profile: name, tenure, tier and prior dispute count.

    Args:
        customer_id: The customer identifier, e.g. "C001".
    """
    return _case().customer.model_dump()


def get_transactions(customer_id: str, limit: int = 20) -> list[dict]:
    """Return the customer's recent transactions, newest first.

    Args:
        customer_id: The customer identifier, e.g. "C001".
        limit: Maximum number of transactions to return.
    """
    return [t.model_dump() for t in _case().transactions[:limit]]


def get_dispute(dispute_id: str) -> dict:
    """Return the dispute record, including the customer's own written statement.

    Args:
        dispute_id: The dispute identifier, e.g. "D001".
    """
    return _case().dispute.model_dump()


def fraud_score(txn_id: str) -> dict:
    """Return a fraud risk score from 0 (benign) to 100 (near-certain fraud), with reason codes.

    Args:
        txn_id: The transaction identifier, e.g. "T1".
    """
    return _case().fraud.model_dump()


def kyc_status(customer_id: str) -> dict:
    """Return the customer's identity-verification status and any analyst notes.

    Args:
        customer_id: The customer identifier, e.g. "C001".
    """
    return _case().kyc.model_dump()


def execute_action(dispute_id: str, action: str, justification: str) -> dict:
    """Record the final decision and end the case. Call this exactly once.

    Args:
        dispute_id: The dispute identifier, e.g. "D001".
        action: One of REFUND, DENY, ESCALATE_TO_HUMAN, REQUEST_DOCUMENTS.
        justification: One or two sentences explaining the decision.
    """
    act = Action(action)
    _ACTION_LOG.append({"dispute_id": dispute_id, "action": act.value, "justification": justification})
    if len(_ACTION_LOG) > 1:
        # The binding decision was already made; repeat calls change nothing.
        # Say so plainly so the agent stops instead of looping.
        return {
            "status": "already_recorded",
            "action": _ACTION_LOG[0]["action"],
            "note": "A decision was already recorded for this dispute and cannot be changed. "
                    "Do not call execute_action again. Reply with a one-line summary and stop.",
        }
    return {"status": "recorded", "action": act.value,
            "note": "Decision recorded. Do not call execute_action again. "
                    "Reply with a one-line summary and stop."}


ALL_TOOLS = [get_customer, get_transactions, get_dispute, fraud_score, kyc_status, execute_action]
