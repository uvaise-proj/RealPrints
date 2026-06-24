from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator

from app.models.process_log import ProcessType


# ── Per-stage data schemas ─────────────────────────────────────────────────────

class FusingData(BaseModel):
    fusing_temp: float = Field(..., gt=0, description="Fusing temperature in °C")
    printing_temp: float = Field(..., gt=0, description="Printing temperature in °C")
    paint_name: str = Field(..., min_length=1, max_length=255)


class ExposingData(BaseModel):
    frame_size: str = Field(..., min_length=1, max_length=100)
    mesh_count: int = Field(..., gt=0)
    quality: str = Field(..., min_length=1, max_length=100)


class PrintingData(BaseModel):
    print_material: str = Field(..., min_length=1, max_length=255)
    paper_size: str = Field(..., min_length=1, max_length=100)
    ink_type: str = Field(..., min_length=1, max_length=100)
    ink_color: str = Field(..., min_length=1, max_length=100)
    paper_quantity: int = Field(..., gt=0)
    gel_or_powder: str = Field(..., min_length=1, max_length=100)


class CuttingData(BaseModel):
    no_of_pieces: int = Field(..., gt=0)
    no_of_ups: int = Field(..., gt=0)


_STAGE_VALIDATORS: dict[ProcessType, type[BaseModel]] = {
    ProcessType.fusing: FusingData,
    ProcessType.exposing: ExposingData,
    ProcessType.printing: PrintingData,
    ProcessType.cutting: CuttingData,
}


# ── Request / response schemas ─────────────────────────────────────────────────

class ProcessCreate(BaseModel):
    project_id: str = Field(..., min_length=1, max_length=100)
    process_type: ProcessType
    data: dict[str, Any]

    @model_validator(mode="after")
    def validate_stage_data(self) -> "ProcessCreate":
        validator_cls = _STAGE_VALIDATORS[self.process_type]
        validator_cls.model_validate(self.data)
        return self


class ProcessLogResponse(BaseModel):
    id: int
    project_id: str
    process_type: ProcessType
    data: dict[str, Any]
    timestamp: datetime

    model_config = {"from_attributes": True}


class ProjectProcessResponse(BaseModel):
    project_id: str
    total: int
    stages: list[ProcessLogResponse]
