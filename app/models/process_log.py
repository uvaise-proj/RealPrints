import enum

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database import Base


class ProcessType(str, enum.Enum):
    fusing = "fusing"
    exposing = "exposing"
    printing = "printing"
    cutting = "cutting"


class ProcessLog(Base):
    __tablename__ = "process_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        String(100),
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )
    operator_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    process_type = Column(SAEnum(ProcessType), nullable=False)
    data = Column(JSONB, nullable=False)
    quality_rating = Column(Integer, nullable=True)       # 1–5, recorded after QC
    success = Column(Boolean, default=False, nullable=False)
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "quality_rating IS NULL OR (quality_rating >= 1 AND quality_rating <= 5)",
            name="chk_process_quality_rating_range",
        ),
        Index("ix_process_logs_project_id", "project_id"),
        Index("ix_process_logs_process_type", "process_type"),
        Index("ix_process_logs_project_type", "project_id", "process_type"),
        Index("ix_process_logs_success_quality", "success", "quality_rating"),
    )
