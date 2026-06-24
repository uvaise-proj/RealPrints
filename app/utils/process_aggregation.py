"""
Shared aggregation helpers for process-log analytics and recommendations.

Centralised here so both recommendation_service and analytics_service
use the same field taxonomy and aggregation rules.
"""
from collections import Counter
from typing import Any

from app.models.process_log import ProcessType

# Which JSONB fields to aggregate per stage, and how.
# numeric → arithmetic mean  |  categorical → mode (most frequent value)
STAGE_FIELD_TYPES: dict[ProcessType, dict[str, list[str]]] = {
    ProcessType.fusing: {
        "numeric":     ["fusing_temp", "printing_temp"],
        "categorical": ["paint_name"],
    },
    ProcessType.exposing: {
        "numeric":     ["mesh_count"],
        "categorical": ["frame_size", "quality"],
    },
    ProcessType.printing: {
        "numeric":     ["paper_quantity"],
        "categorical": ["print_material", "paper_size", "ink_type", "ink_color", "gel_or_powder"],
    },
    ProcessType.cutting: {
        "numeric":     ["no_of_pieces", "no_of_ups"],
        "categorical": [],
    },
}


def mode(values: list[Any]) -> Any:
    """Return the most frequent value; first-seen wins on tie."""
    return Counter(values).most_common(1)[0][0]


def aggregate(data_rows: list[dict[str, Any]], process_type: ProcessType) -> dict[str, Any]:
    """
    Aggregate a list of JSONB data dicts for the given process type.
    Numeric fields → mean (rounded to 2 dp).
    Categorical fields → mode.
    Fields missing or None in a row are skipped for that row only.
    """
    field_types = STAGE_FIELD_TYPES[process_type]
    result: dict[str, Any] = {}

    for field in field_types["numeric"]:
        vals = [row[field] for row in data_rows if field in row and row[field] is not None]
        if vals:
            result[field] = round(sum(vals) / len(vals), 2)

    for field in field_types["categorical"]:
        vals = [row[field] for row in data_rows if field in row and row[field] is not None]
        if vals:
            result[field] = mode(vals)

    return result
