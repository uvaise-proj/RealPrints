from __future__ import annotations

import enum
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


# ── Enums (mirror models, kept in schemas for Pydantic validation) ─────────────

class GarmentMaterial(str, enum.Enum):
    cotton = "cotton"
    polyester = "polyester"
    blend = "blend"
    nylon = "nylon"


class FabricColour(str, enum.Enum):
    light = "light"
    dark = "dark"


class Texture(str, enum.Enum):
    smooth = "smooth"
    rough = "rough"
    stretchable = "stretchable"


class StickerType(str, enum.Enum):
    vinyl = "vinyl"
    sublimation = "sublimation"
    heat_transfer = "heat_transfer"


class PressureLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class PeelType(str, enum.Enum):
    hot = "hot"
    cold = "cold"
    warm = "warm"


# ── Nested helper ──────────────────────────────────────────────────────────────

class SizeSchema(BaseModel):
    width: float = Field(..., gt=0, description="Width in cm")
    height: float = Field(..., gt=0, description="Height in cm")


# ── Request schemas ────────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    # Basic Info
    project_id: str = Field(..., min_length=1, max_length=100, examples=["PRJ-001"])
    client_name: str = Field(..., min_length=1, max_length=255)
    date: date
    order_quantity: int = Field(..., gt=0)

    # Material & Surface
    garment_material: GarmentMaterial
    fabric_weight_gsm: Optional[float] = Field(None, gt=0)
    fabric_colour: FabricColour
    texture: Texture

    # Sticker / Print
    sticker_type: StickerType
    size: SizeSchema
    shape: Optional[str] = Field(None, max_length=100)
    colour_layers: Optional[int] = Field(None, ge=1)
    ink_type: Optional[str] = Field(None, max_length=100)

    # Machine Settings
    press_temperature: float = Field(..., gt=0, description="Press temperature in °C")
    press_time: float = Field(..., gt=0, description="Press time in seconds")
    pressure_level: PressureLevel
    peel_type: PeelType

    # Process
    pre_press_required: bool = False
    cooling_time: Optional[float] = Field(None, ge=0, description="Cooling time in seconds")
    layering_steps: Optional[int] = Field(None, ge=1)

    # Outcome
    quality_rating: Optional[int] = Field(None, ge=1, le=5)
    issues: Optional[str] = None
    rework: bool = False
    final_approved: bool = False


# ── Response schemas ───────────────────────────────────────────────────────────

class ProjectResponse(BaseModel):
    project_id: str
    client_name: str
    date: date
    order_quantity: int

    garment_material: GarmentMaterial
    fabric_weight_gsm: Optional[float]
    fabric_colour: FabricColour
    texture: Texture

    sticker_type: StickerType
    size_width_cm: float
    size_height_cm: float
    shape: Optional[str]
    colour_layers: Optional[int]
    ink_type: Optional[str]

    press_temperature: float
    press_time: float
    pressure_level: PressureLevel
    peel_type: PeelType

    pre_press_required: bool
    cooling_time: Optional[float]
    layering_steps: Optional[int]

    quality_rating: Optional[int]
    issues: Optional[str]
    rework: bool
    final_approved: bool

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[ProjectResponse]


# ── Filter schema (used internally by the service layer) ──────────────────────

class ProjectFilter(BaseModel):
    client_name: Optional[str] = None
    garment_material: Optional[GarmentMaterial] = None
    sticker_type: Optional[StickerType] = None
    fabric_colour: Optional[FabricColour] = None
    final_approved: Optional[bool] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


# ── Recommendation schemas ─────────────────────────────────────────────────────

class RecommendRequest(BaseModel):
    garment_material: GarmentMaterial
    sticker_type: StickerType
    fabric_colour: FabricColour
    texture: Optional[Texture] = None
    fabric_weight_gsm: Optional[float] = Field(None, gt=0)


class RecommendationItem(BaseModel):
    project_id: str
    press_temperature: float
    press_time: float
    pressure_level: PressureLevel
    peel_type: PeelType
    quality_rating: Optional[int]
    match_score: float = Field(..., description="Relevance score between 0 and 1")

    model_config = {"from_attributes": True}


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]
    total_matches: int
    message: str
