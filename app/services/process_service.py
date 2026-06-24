import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.models.process_log import ProcessLog, ProcessType
from app.schemas.process_log import ProcessCreate

logger = logging.getLogger(__name__)


def add_process_log(
    db: Session,
    data: ProcessCreate,
    operator_id: int | None = None,
) -> ProcessLog:
    log = ProcessLog(
        project_id=data.project_id,
        operator_id=operator_id,
        process_type=data.process_type.value,
        data=data.data,
        quality_rating=data.quality_rating,
        success=data.success,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    logger.info(
        "Process log created: id=%s project=%s type=%s operator=%s",
        log.id, log.project_id, log.process_type, operator_id,
    )
    return log


def get_process_logs(
    db: Session,
    project_id: str,
    process_type: Optional[ProcessType] = None,
) -> list[ProcessLog]:
    query = db.query(ProcessLog).filter(ProcessLog.project_id == project_id)
    if process_type:
        query = query.filter(ProcessLog.process_type == process_type)
    return query.order_by(ProcessLog.timestamp.asc()).all()
