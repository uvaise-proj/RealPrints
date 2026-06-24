import logging
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import (
    RecommendRequest, RecommendationItem, RecommendResponse, PressureLevel, PeelType,
)

logger = logging.getLogger(__name__)

# Contribution of each attribute to the total match score (must sum to 1.0)
_WEIGHT_MATERIAL = 0.40
_WEIGHT_STICKER  = 0.35
_WEIGHT_COLOUR   = 0.25


def _score(project: Project, req: RecommendRequest) -> float:
    """Return a 0–1 relevance score for a project against the request."""
    score = 0.0
    if project.garment_material == req.garment_material.value:
        score += _WEIGHT_MATERIAL
    if project.sticker_type == req.sticker_type.value:
        score += _WEIGHT_STICKER
    if project.fabric_colour == req.fabric_colour.value:
        score += _WEIGHT_COLOUR
    return round(score, 4)


def get_recommendations(
    db: Session,
    request: RecommendRequest,
    top_n: int = 3,
) -> RecommendResponse:
    # Only consider projects that were approved — they represent successful outcomes
    candidates = (
        db.query(Project)
        .filter(Project.final_approved == True)
        .filter(
            (Project.garment_material == request.garment_material.value)
            | (Project.sticker_type == request.sticker_type.value)
            | (Project.fabric_colour == request.fabric_colour.value)
        )
        .all()
    )

    if not candidates:
        return RecommendResponse(
            recommendations=[],
            total_matches=0,
            message="No approved matching projects found. Try different parameters.",
        )

    # Sort by (match_score DESC, quality_rating DESC) so high-quality exact matches surface first
    scored = sorted(
        [(p, _score(p, request)) for p in candidates],
        key=lambda x: (x[1], x[0].quality_rating or 0),
        reverse=True,
    )

    recommendations = [
        RecommendationItem(
            project_id=p.project_id,
            press_temperature=p.press_temperature,
            press_time=p.press_time,
            pressure_level=PressureLevel(p.pressure_level),
            peel_type=PeelType(p.peel_type),
            quality_rating=p.quality_rating,
            match_score=score,
        )
        for p, score in scored[:top_n]
    ]

    logger.info(
        "Returning %d recommendations from %d candidates for material=%s sticker=%s colour=%s",
        len(recommendations), len(candidates),
        request.garment_material, request.sticker_type, request.fabric_colour,
    )
    return RecommendResponse(
        recommendations=recommendations,
        total_matches=len(candidates),
        message=f"Top {len(recommendations)} recommendation(s) from {len(candidates)} approved match(es).",
    )
