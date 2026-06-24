import logging
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.project import (
    FabricColour, GarmentMaterial, ProjectCreate,
    ProjectListResponse, ProjectResponse, StickerType, ProjectFilter,
)
from app.services import project_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new printing project",
)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    try:
        return project_service.create_project(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get(
    "/",
    response_model=ProjectListResponse,
    summary="List / search projects with optional filters",
)
def list_projects(
    client_name: Optional[str] = Query(None, description="Partial match on client name"),
    garment_material: Optional[GarmentMaterial] = Query(None),
    sticker_type: Optional[StickerType] = Query(None),
    fabric_colour: Optional[FabricColour] = Query(None),
    final_approved: Optional[bool] = Query(None),
    date_from: Optional[date] = Query(None, description="Inclusive start date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Inclusive end date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Number of records to skip (pagination)"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    filters = ProjectFilter(
        client_name=client_name,
        garment_material=garment_material,
        sticker_type=sticker_type,
        fabric_colour=fabric_colour,
        final_approved=final_approved,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )
    projects, total = project_service.get_projects(db, filters)
    return ProjectListResponse(total=total, skip=skip, limit=limit, data=projects)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Fetch a single project by its ID",
)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = project_service.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found.",
        )
    return project
