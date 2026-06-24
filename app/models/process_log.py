import enum

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
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
    process_type = Column(SAEnum(ProcessType), nullable=False)
    data = Column(JSONB, nullable=False)
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_process_logs_project_id", "project_id"),
        Index("ix_process_logs_process_type", "process_type"),
        Index("ix_process_logs_project_type", "project_id", "process_type"),
    )
