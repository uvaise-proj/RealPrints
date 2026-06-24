import enum
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, Date,
    Enum as SAEnum, CheckConstraint,
)
from app.database import Base


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


class Project(Base):
    __tablename__ = "projects"

    # ── Basic Info ────────────────────────────────────────────────────────────
    project_id = Column(String(100), primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    order_quantity = Column(Integer, nullable=False)

    # ── Material & Surface ────────────────────────────────────────────────────
    garment_material = Column(SAEnum(GarmentMaterial), nullable=False)
    fabric_weight_gsm = Column(Float, nullable=True)
    fabric_colour = Column(SAEnum(FabricColour), nullable=False)
    texture = Column(SAEnum(Texture), nullable=False)

    # ── Sticker / Print ───────────────────────────────────────────────────────
    sticker_type = Column(SAEnum(StickerType), nullable=False)
    size_width_cm = Column(Float, nullable=False)
    size_height_cm = Column(Float, nullable=False)
    shape = Column(String(100), nullable=True)
    colour_layers = Column(Integer, nullable=True)
    ink_type = Column(String(100), nullable=True)

    # ── Machine Settings ──────────────────────────────────────────────────────
    press_temperature = Column(Float, nullable=False)   # °C
    press_time = Column(Float, nullable=False)           # seconds
    pressure_level = Column(SAEnum(PressureLevel), nullable=False)
    peel_type = Column(SAEnum(PeelType), nullable=False)

    # ── Process ───────────────────────────────────────────────────────────────
    pre_press_required = Column(Boolean, default=False, nullable=False)
    cooling_time = Column(Float, nullable=True)          # seconds
    layering_steps = Column(Integer, nullable=True)

    # ── Outcome ───────────────────────────────────────────────────────────────
    quality_rating = Column(Integer, nullable=True)      # 1–5
    issues = Column(Text, nullable=True)
    rework = Column(Boolean, default=False, nullable=False)
    final_approved = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("order_quantity > 0", name="chk_order_quantity_positive"),
        CheckConstraint(
            "quality_rating IS NULL OR (quality_rating >= 1 AND quality_rating <= 5)",
            name="chk_quality_rating_range",
        ),
        CheckConstraint("press_temperature > 0", name="chk_temperature_positive"),
        CheckConstraint("press_time > 0", name="chk_press_time_positive"),
    )
