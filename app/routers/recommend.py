import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.process_log import StageRecommendRequest, StageRecommendResponse
from app.schemas.project import RecommendRequest, RecommendResponse
from app.services import recommendation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommend", tags=["Recommendations"])


@router.post(
    "/",
    response_model=RecommendResponse,
    summary="Suggest optimal machine settings based on material and sticker type",
)
def recommend(
    payload: RecommendRequest,
    top_n: int = Query(3, ge=1, le=10, description="Number of recommendations to return"),
    db: Session = Depends(get_db),
):
    return recommendation_service.get_recommendations(db, payload, top_n=top_n)


@router.post(
    "/stage",
    response_model=StageRecommendResponse,
    summary="Recommend optimal stage parameters from historical successful process logs",
)
def recommend_stage(payload: StageRecommendRequest, db: Session = Depends(get_db)):
    return recommendation_service.get_stage_recommendations(db, payload)
