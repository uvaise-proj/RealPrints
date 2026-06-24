import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.process_log import ProcessType
from app.models.user import User
from app.schemas.process_log import ProcessCreate, ProcessLogResponse, ProjectProcessResponse
from app.services import process_service, project_service
from app.services.auth_service import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/process", tags=["Process Logs"])


@router.post(
    "/",
    response_model=ProcessLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a process stage log to a project",
)
def add_process(
    payload:      ProcessCreate,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    project = project_service.get_project_by_id(db, payload.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{payload.project_id}' not found.",
        )
    return process_service.add_process_log(db, payload, operator_id=current_user.id)


@router.get(
    "/{project_id}",
    response_model=ProjectProcessResponse,
    summary="Fetch all process stage logs for a project",
)
def get_process_logs(
    project_id:   str,
    process_type: Optional[ProcessType] = Query(None, description="Filter by stage type"),
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    project = project_service.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found.",
        )
    logs = process_service.get_process_logs(db, project_id, process_type)
    return ProjectProcessResponse(project_id=project_id, total=len(logs), stages=logs)
