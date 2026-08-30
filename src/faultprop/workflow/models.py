"""Data models for the synthetic card-dispute triage workflow.

Plain-language summary: a Case is one customer dispute plus the correct answer.
Everything the tools return is derived from the Case, so the harness controls
all ground truth.
"""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Action(str, Enum):
    REFUND = "REFUND"                      # money moves — a wrong REFUND is a silent failure
    DENY = "DENY"                          # money-affecting — a wrong DENY harms the customer
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"  # safe failure
    REQUEST_DOCUMENTS = "REQUEST_DOCUMENTS"  # safe failure


MONEY_MOVING = {Action.REFUND, Action.DENY}


class Transaction(BaseModel):
    txn_id: str
    merchant: str
    amount: float
    date: str            # ISO date, synthetic
    channel: str         # "card_present" | "online" | "recurring"


class Customer(BaseModel):
    customer_id: str
    name: str            # synthetic (Faker) — never real
    tenure_months: int
    prior_disputes: int
    tier: str            # "standard" | "premium"


class Dispute(BaseModel):
    dispute_id: str
    txn_id: str
    customer_statement: str   # free text — the injection surface for adversarial faults
    filed_date: str


class FraudScore(BaseModel):
    score: int = Field(ge=0, le=100)
    reason_codes: list[str]


class KycStatus(BaseModel):
    verified: bool
    last_verified: str
    notes: str = ""           # second injection surface (POISONED_TOOL_DOC)


class Case(BaseModel):
    """One hand-written scenario with ground truth."""
    case_id: str
    customer: Customer
    transactions: list[Transaction]
    dispute: Dispute
    fraud: FraudScore
    kyc: KycStatus
    correct_action: Action
    rationale: str            # why correct_action is correct (for the paper & for hand checks)
    ambiguous: bool = False   # True → ESCALATE is the expected safe answer
