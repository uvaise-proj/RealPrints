import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectFilter

logger = logging.getLogger(__name__)


def create_project(db: Session, data: ProjectCreate) -> Project:
    if db.query(Project).filter(Project.project_id == data.project_id).first():
        raise ValueError(f"Project ID '{data.project_id}' already exists.")

    project = Project(
        project_id=data.project_id,
        client_name=data.client_name,
        date=data.date,
        start_date=data.start_date,
        end_date=data.end_date,
        order_quantity=data.order_quantity,
        garment_material=data.garment_material.value,
        fabric_weight_gsm=data.fabric_weight_gsm,
        fabric_colour=data.fabric_colour.value,
        texture=data.texture.value,
        sticker_type=data.sticker_type.value,
        size_width_cm=data.size.width,
        size_height_cm=data.size.height,
        shape=data.shape,
        colour_layers=data.colour_layers,
        ink_type=data.ink_type,
        press_temperature=data.press_temperature,
        press_time=data.press_time,
        pressure_level=data.pressure_level.value,
        peel_type=data.peel_type.value,
        pre_press_required=data.pre_press_required,
        cooling_time=data.cooling_time,
        layering_steps=data.layering_steps,
        quality_rating=data.quality_rating,
        issues=data.issues,
        rework=data.rework,
        final_approved=data.final_approved,
    )

    db.add(project)
    db.commit()
    db.refresh(project)
    logger.info("Created project %s for client '%s'", project.project_id, project.client_name)
    return project


def get_project_by_id(db: Session, project_id: str) -> Optional[Project]:
    return db.query(Project).filter(Project.project_id == project_id).first()


def get_projects(db: Session, filters: ProjectFilter) -> tuple[list[Project], int]:
    query = db.query(Project)

    if filters.client_name:
        query = query.filter(Project.client_name.ilike(f"%{filters.client_name}%"))
    if filters.garment_material:
        query = query.filter(Project.garment_material == filters.garment_material.value)
    if filters.sticker_type:
        query = query.filter(Project.sticker_type == filters.sticker_type.value)
    if filters.fabric_colour:
        query = query.filter(Project.fabric_colour == filters.fabric_colour.value)
    if filters.final_approved is not None:
        query = query.filter(Project.final_approved == filters.final_approved)
    if filters.date_from:
        query = query.filter(Project.date >= filters.date_from)
    if filters.date_to:
        query = query.filter(Project.date <= filters.date_to)

    total = query.count()
    projects = (
        query.order_by(Project.date.desc())
        .offset(filters.skip)
        .limit(filters.limit)
        .all()
    )
    return projects, total
