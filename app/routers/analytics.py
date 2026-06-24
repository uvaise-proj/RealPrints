import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.process_log import ProcessType
from app.schemas.analytics import BestConfigResponse, FailureRateResponse, SummaryResponse
from app.schemas.project import GarmentMaterial
from app.services import analytics_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/failure-rate",
    response_model=FailureRateResponse,
    summary="Failure rate for a process stage, optionally filtered by garment material",
)
def failure_rate(
    process_type: ProcessType = Query(..., description="Stage to analyse"),
    garment_material: Optional[GarmentMaterial] = Query(None, description="Limit to one material"),
    db: Session = Depends(get_db),
):
    return analytics_service.get_failure_rate(db, process_type, garment_material)


@router.get(
    "/best-config",
    response_model=BestConfigResponse,
    summary="Best stage configuration from successful high-quality logs",
)
def best_config(
    process_type: ProcessType = Query(..., description="Stage to analyse"),
    garment_material: Optional[GarmentMaterial] = Query(None, description="Limit to one material"),
    db: Session = Depends(get_db),
):
    return analytics_service.get_best_config(db, process_type, garment_material)


@router.get(
    "/summary",
    response_model=SummaryResponse,
    summary="System-wide production summary with per-stage breakdown",
)
def summary(
    garment_material: Optional[GarmentMaterial] = Query(None, description="Scope summary to one material"),
    db: Session = Depends(get_db),
):
    return analytics_service.get_summary(db, garment_material)
