import logging
from typing import Optional

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.process_log import ProcessLog, ProcessType
from app.models.project import Project
from app.schemas.analytics import (
    BestConfigResponse,
    FailureRateResponse,
    StageDistributionItem,
    SummaryResponse,
)
from app.schemas.project import GarmentMaterial
from app.utils.process_aggregation import aggregate

logger = logging.getLogger(__name__)


# ── Shared query helper ────────────────────────────────────────────────────────

def _apply_filters(query, process_type: ProcessType, garment_material: Optional[GarmentMaterial]):
    """Apply the common process_type + optional garment_material filters."""
    query = query.filter(ProcessLog.process_type == process_type.value)
    if garment_material:
        query = (
            query
            .join(Project, ProcessLog.project_id == Project.project_id)
            .filter(Project.garment_material == garment_material.value)
        )
    return query


# ── A) Failure rate ────────────────────────────────────────────────────────────

def get_failure_rate(
    db: Session,
    process_type: ProcessType,
    garment_material: Optional[GarmentMaterial] = None,
) -> FailureRateResponse:
    """
    Single aggregating query:
      COUNT(*) for total runs
      SUM(CASE WHEN success IS FALSE THEN 1 ELSE 0) for failed runs
    Joined to projects only when a garment_material filter is requested.
    """
    base = db.query(
        func.count(ProcessLog.id).label("total"),
        func.sum(
            case((ProcessLog.success.is_(False), 1), else_=0)
        ).label("failed"),
    )

    if garment_material:
        base = (
            base
            .join(Project, ProcessLog.project_id == Project.project_id)
            .filter(Project.garment_material == garment_material.value)
        )

    base = base.filter(ProcessLog.process_type == process_type.value)
    row  = base.one()

    total   = int(row.total  or 0)
    failed  = int(row.failed or 0)
    success = total - failed

    logger.info("failure-rate: type=%s material=%s total=%d failed=%d",
                process_type.value, garment_material, total, failed)

    return FailureRateResponse(
        process_type=process_type,
        garment_material=garment_material,
        total_runs=total,
        success_runs=success,
        failed_runs=failed,
        failure_rate=round(failed / total, 4) if total > 0 else 0.0,
    )


# ── B) Best config ─────────────────────────────────────────────────────────────

def get_best_config(
    db: Session,
    process_type: ProcessType,
    garment_material: Optional[GarmentMaterial] = None,
) -> BestConfigResponse:
    """
    Fetch all successful (success=True, quality_rating>=4) logs for the stage,
    then aggregate JSONB fields: mean for numeric, mode for categorical.
    """
    query = (
        db.query(ProcessLog)
        .join(Project, ProcessLog.project_id == Project.project_id)
        .filter(ProcessLog.process_type == process_type.value)
        .filter(ProcessLog.success.is_(True))
        .filter(ProcessLog.quality_rating >= 4)
    )
    if garment_material:
        query = query.filter(Project.garment_material == garment_material.value)

    logs = query.all()
    material_label = garment_material.value if garment_material else "all materials"

    if not logs:
        logger.info("best-config: no data for type=%s material=%s", process_type.value, material_label)
        return BestConfigResponse(
            process_type=process_type,
            garment_material=garment_material,
            best_config={},
            average_quality=None,
            sample_count=0,
            message=(
                f"No successful {process_type.value} logs found for {material_label}. "
                "Log more successful stages to generate a best config."
            ),
        )

    best_config     = aggregate([log.data for log in logs], process_type)
    quality_ratings = [log.quality_rating for log in logs if log.quality_rating is not None]
    avg_quality     = round(sum(quality_ratings) / len(quality_ratings), 2) if quality_ratings else None

    logger.info("best-config: type=%s material=%s samples=%d avg_q=%s",
                process_type.value, material_label, len(logs), avg_quality)

    return BestConfigResponse(
        process_type=process_type,
        garment_material=garment_material,
        best_config=best_config,
        average_quality=avg_quality,
        sample_count=len(logs),
        message=(
            f"Best config derived from {len(logs)} successful "
            f"{process_type.value} log(s) for {material_label}."
        ),
    )


# ── C) Summary ─────────────────────────────────────────────────────────────────

def get_summary(
    db: Session,
    garment_material: Optional[GarmentMaterial] = None,
) -> SummaryResponse:
    """
    Three focused queries:
      1. Total project count (scalar)
      2. Overall success / failure counts (single aggregating query)
      3. Per-stage distribution with per-stage success counts (GROUP BY)
    """
    # 1. Project count
    project_query = db.query(func.count(Project.project_id))
    if garment_material:
        project_query = project_query.filter(
            Project.garment_material == garment_material.value
        )
    total_projects = int(project_query.scalar() or 0)

    # 2. Overall log stats — join projects only when filtering by material
    stats_query = db.query(
        func.count(ProcessLog.id).label("total"),
        func.sum(case((ProcessLog.success.is_(True), 1), else_=0)).label("successful"),
    )
    if garment_material:
        stats_query = (
            stats_query
            .join(Project, ProcessLog.project_id == Project.project_id)
            .filter(Project.garment_material == garment_material.value)
        )
    stats = stats_query.one()

    total_logs  = int(stats.total      or 0)
    successful  = int(stats.successful or 0)
    failed      = total_logs - successful
    success_rate = round(successful / total_logs, 4) if total_logs > 0 else 0.0

    # 3. Per-stage distribution with success counts
    dist_query = db.query(
        ProcessLog.process_type,
        func.count(ProcessLog.id).label("total"),
        func.sum(case((ProcessLog.success.is_(True), 1), else_=0)).label("success_count"),
    ).group_by(ProcessLog.process_type)

    if garment_material:
        dist_query = (
            dist_query
            .join(Project, ProcessLog.project_id == Project.project_id)
            .filter(Project.garment_material == garment_material.value)
        )

    stage_distribution = []
    for row in dist_query.all():
        row_total   = int(row.total        or 0)
        row_success = int(row.success_count or 0)
        row_failed  = row_total - row_success

        # SAEnum returns the Python enum member directly; guard against raw strings
        pt = row.process_type
        if isinstance(pt, str):
            pt = ProcessType(pt)

        stage_distribution.append(
            StageDistributionItem(
                process_type=pt,
                total=row_total,
                success_count=row_success,
                failed_count=row_failed,
                success_rate=round(row_success / row_total, 4) if row_total > 0 else 0.0,
            )
        )

    # Sort by stage definition order for consistent output
    _ORDER = list(ProcessType)
    stage_distribution.sort(key=lambda x: _ORDER.index(x.process_type))

    logger.info(
        "summary: projects=%d logs=%d success_rate=%.4f material=%s",
        total_projects, total_logs, success_rate, garment_material,
    )

    return SummaryResponse(
        total_projects=total_projects,
        total_process_logs=total_logs,
        successful_runs=successful,
        failed_runs=failed,
        overall_success_rate=success_rate,
        stage_distribution=stage_distribution,
    )
