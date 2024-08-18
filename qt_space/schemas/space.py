from ninja import Field, ModelSchema, Schema

from qt_space.models import Space


class RoomRequestSchema(Schema):
    name: str = Field(..., max_length=256)
    description: str | None = Field(default=None, max_length=2048)
    hemisphere: Space.HemispheresChoices | None = None
    temperature: int = Field(default=Space.DEFAULT_TEMPERATURE, ge=-273, le=100)
    humidity: int = Field(default=Space.DEFAULT_HUMIDITY, ge=0, le=100)
    window_side: Space.CardinalDirectionChoices | None = None


class RoomResponseSchema(ModelSchema):
    class Meta:
        model = Space
        exclude = ('user',)


ListSpaceResponseSchema = list[RoomResponseSchema]
