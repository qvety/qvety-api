import typing as t

from ninja import FilterSchema


class GardenFilter(FilterSchema):
    room_id: t.Optional[int] = None
