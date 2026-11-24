import itertools
import uuid
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator


class RouteSchema(BaseModel):
    route_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(..., description="The name of the route")
    puv_type: str = Field(..., description="The PUV type code, e.g. traditional_jeepney")


class RouteResponseSchema(RouteSchema):
    id: uuid.UUID = Field(..., description="The ID of the route")


class RouteCreate(RouteSchema):
    pass


class RouteEdit(RouteSchema):
    pass


class RouteStopsEdit(BaseModel):
    stop_ids: list[uuid.UUID] = Field(..., min_length=2, description="The route's stops in travel order")

    @field_validator("stop_ids")
    @classmethod
    def no_consecutive_repeats(cls, ids: list[uuid.UUID]) -> list[uuid.UUID]:
        """A stop twice in a row is a 0 km segment. Loop routes (a later repeat) stay allowed."""
        if any(a == b for a, b in itertools.pairwise(ids)):
            raise ValueError("a stop can't follow itself")
        return ids


class RouteStopResponseSchema(BaseModel):
    stop_id: uuid.UUID
    name: str
    stop_sequence: int
    distance_from_previous_km: float | None


class RouteDetailSchema(RouteResponseSchema):
    stops: list[RouteStopResponseSchema]


class RouteListItemSchema(RouteResponseSchema):
    stop_count: int
