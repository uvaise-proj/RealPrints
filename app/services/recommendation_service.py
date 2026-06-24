import logging

from sqlalchemy.orm import Session

from app.models.process_log import ProcessLog, ProcessType
from app.models.project import Project
from app.schemas.process_log import StageRecommendRequest, StageRecommendResponse
from app.schemas.project import (
    RecommendRequest, RecommendationItem, RecommendResponse, PressureLevel, PeelType,
)
from app.utils.process_aggregation import aggregate

logger = logging.getLogger(__name__)

# Contribution of each attribute to the total match score (must sum to 1.0)
_WEIGHT_MATERIAL = 0.40
_WEIGHT_STICKER  = 0.35
_WEIGHT_COLOUR   = 0.25


def _score(project: Project, req: RecommendRequest) -> float:
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


# ── Stage-wise recommendation engine ──────────────────────────────────────────

_FULL_CONFIDENCE_SAMPLES = 10


def _compute_confidence(n_samples: int, mean_quality: float) -> float:
    """
    Blend volume (60%) and quality (40%) into a 0–1 confidence score.
    Volume caps at _FULL_CONFIDENCE_SAMPLES. Quality is normalised over 4–5.
    """
    volume_score  = min(1.0, n_samples / _FULL_CONFIDENCE_SAMPLES)
    quality_score = max(0.0, mean_quality - 4.0)   # 4 → 0.0, 5 → 1.0
    return round(volume_score * 0.6 + quality_score * 0.4, 4)


def _query_stage_logs(
    db: Session,
    process_type: ProcessType,
    garment_material_value: str,
    colour_layers: int | None,
) -> list[ProcessLog]:
    q = (
        db.query(ProcessLog)
        .join(Project, ProcessLog.project_id == Project.project_id)
        .filter(ProcessLog.process_type == process_type.value)
        .filter(ProcessLog.success.is_(True))
        .filter(ProcessLog.quality_rating >= 4)
        .filter(Project.garment_material == garment_material_value)
    )
    if colour_layers is not None:
        q = q.filter(Project.colour_layers == colour_layers)
    return q.all()


def get_stage_recommendations(
    db: Session,
    request: StageRecommendRequest,
) -> StageRecommendResponse:
    material_val = request.garment_material.value

    logs = _query_stage_logs(db, request.process_type, material_val, request.image_color_count)
    colour_relaxed = False

    if not logs and request.image_color_count is not None:
        logs = _query_stage_logs(db, request.process_type, material_val, None)
        colour_relaxed = True

    if not logs:
        logger.info("No stage logs: process_type=%s garment=%s", request.process_type.value, material_val)
        return StageRecommendResponse(
            process_type=request.process_type,
            recommended_values={},
            confidence=0.0,
            based_on_samples=0,
            message=(
                f"No successful {request.process_type.value} logs found for "
                f"{material_val} garments. Log more successful stages to enable recommendations."
            ),
        )

    data_rows       = [log.data for log in logs]
    recommended     = aggregate(data_rows, request.process_type)
    quality_ratings = [log.quality_rating for log in logs if log.quality_rating is not None]
    mean_quality    = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 4.0
    confidence      = _compute_confidence(len(logs), mean_quality)

    msg = (
        f"Based on {len(logs)} successful {request.process_type.value} "
        f"log(s) for {material_val} garments."
    )
    if colour_relaxed:
        msg += (
            f" Colour count filter relaxed — no exact matches for "
            f"{request.image_color_count} colour(s)."
        )

    logger.info(
        "Stage recommendation: type=%s material=%s samples=%d confidence=%.4f",
        request.process_type.value, material_val, len(logs), confidence,
    )
    return StageRecommendResponse(
        process_type=request.process_type,
        recommended_values=recommended,
        confidence=confidence,
        based_on_samples=len(logs),
        message=msg,
    )
