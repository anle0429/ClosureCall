from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

Posture = Literal["normal", "delayed_arrival", "early_dismissal", "telework", "closure"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvaluationRequest(StrictModel):
    facility_id: str = Field(min_length=1, max_length=100)
    start: datetime
    end: datetime
    special_shift: bool = False

    @model_validator(mode="after")
    def window(self):
        if self.start.tzinfo is None or self.end.tzinfo is None:
            raise ValueError("Explicit UTC offset required")
        if not 0 < (self.end - self.start).total_seconds() <= 86400:
            raise ValueError("Work period must be positive and at most 24 hours")
        return self


class DecisionRequest(StrictModel):
    snapshot_hash: str = Field(min_length=64, max_length=64)
    action: Literal["approve", "override", "reject"]
    posture: Posture | None = None
    reason: str = Field(default="", max_length=2000)
    timing_at: datetime | None = None
    timing_basis: str = Field(default="", max_length=1000)

    @model_validator(mode="after")
    def human_inputs(self):
        if self.action == "override" and (
            not self.reason.strip() or self.posture is None
        ):
            raise ValueError("Override requires an explicit posture and reason")
        if self.action == "reject" and not self.reason.strip():
            raise ValueError("Reject requires a reason")
        if self.timing_at is not None and self.timing_at.tzinfo is None:
            raise ValueError("Confirmed timing needs an explicit UTC offset")
        return self


class DemoSiteRequest(StrictModel):
    alert_id: str = Field(min_length=1, max_length=1000)


class Assessment(StrictModel):
    recommended_posture: Posture | None
    review_status: Literal["ready_for_manager", "data_incomplete", "unsupported_hazard"]
    rationale_text: str
    matched_rules: list[dict]
    evidence_ids: list[str]
    confidence_label: Literal["low", "moderate", "high"]
    confidence_basis: list[str]
    missing_inputs: list[str]
    what_would_change: list[str]
    protective_action_notice: str
    assumptions: list[str]
    policy_version: str
