from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from app.models.process_log import ProcessType
from app.schemas.project import GarmentMaterial


class FailureRateResponse(BaseModel):
    process_type: ProcessType
    garment_material: Optional[GarmentMaterial] = None
    total_runs: int
    success_runs: int
    failed_runs: int
    failure_rate: float = Field(..., ge=0.0, le=1.0, description="Proportion of failed runs (0–1)")


class BestConfigResponse(BaseModel):
    process_type: ProcessType
    garment_material: Optional[GarmentMaterial] = None
    best_config: dict[str, Any]
    average_quality: Optional[float] = Field(None, ge=1.0, le=5.0)
    sample_count: int
    message: str


class StageDistributionItem(BaseModel):
    process_type: ProcessType
    total: int
    success_count: int
    failed_count: int
    success_rate: float = Field(..., ge=0.0, le=1.0)


class SummaryResponse(BaseModel):
    total_projects: int
    total_process_logs: int
    successful_runs: int
    failed_runs: int
    overall_success_rate: float = Field(..., ge=0.0, le=1.0)
    stage_distribution: list[StageDistributionItem]
