from datetime import date

from ninja import Field, Schema

from qt_garden.models import GardenParameters
from qt_space.schemas.space import RoomResponseSchema


class GardenParametersSchema(Schema):
    last_water: date | None = None
    last_fertilizer: date | None = None
    last_repot: date | None = None
    last_prun: date | None = None

    height: int | None = None
    pot_diameter: int | None = None
    pot_height: int | None = None

    current_state: GardenParameters.StateChoices | None = None
    exposure: GardenParameters.ExposureChoices | None = None


class GardenRequestSchema(Schema):
    room_id: int
    specie_id: int
    parameters: GardenParametersSchema | None = None
    custom_name: str | None = None
    description: str | None = None


class GardenResponseSchema(Schema):
    id: int  # noqa: A003
    latin_name: str = Field(..., alias='specie.latin_name')
    custom_name: str | None = None


class GardenResponseDetailedSchema(GardenResponseSchema):
    room: RoomResponseSchema
    parameters: GardenParametersSchema | None
    description: str | None = None


ListGardenResponseSchema = list[GardenResponseSchema]
