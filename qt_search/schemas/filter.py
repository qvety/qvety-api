import typing as t

from django.db.models import Q, TextChoices
from ninja import Field, FilterSchema
from pydantic.fields import FieldInfo

from qt_search.models import Specie

BIT_FIELD_VALUES = {
    'soil_type',
    'soil_moisture',
    'soil_ph',
    'position_sunlight',
    'position_side',
    'edible_part',
    'fragrance',
    'harvest',
    'planting',
    'foliage',
    'toxicity',
    'habit',
}


class FiltersSchema(FilterSchema):
    search: str = Field(
        None,
        q=[
            'latin_name__icontains',
            'common_names__name__icontains',
            'synonyms__name__icontains'
        ],
    )
    tag: str = Field(None, q=['tags__name__icontains'])

    soil_type: list[Specie.SoilTypeChoices] = None
    soil_moisture: list[Specie.SoilMoistureChoices] = None
    soil_ph: list[Specie.SoilPhChoices] = None

    position_sunlight: list[Specie.PositionSunlightChoices] = None
    position_side: list[Specie.PositionSideChoices] = None

    edible_part: list[Specie.PlantPartsChoices] = None
    fragrance: list[Specie.PlantPartsChoices] = None
    harvest: list[Specie.SeasonsMaxChoices] = None
    planting: list[Specie.SeasonsMaxChoices] = None
    foliage: list[Specie.FoliageTypesChoices] = None
    toxicity: list[Specie.ToxicTypesChoices] = None
    habit: list[Specie.HabitTypesChoices] = None

    exposure: list[Specie.ExposureChoices] = Field(None, q='exposure__in')
    duration: list[Specie.DurationChoices] = Field(None, q='duration__in')

    height_cm_from_gte: int = Field(None, q=['height_cm__from_value__gte'], gt=0)
    height_cm_from_lte: int = Field(None, q=['height_cm__from_value__lte'], gt=0)
    height_cm_to_gte: int = Field(None, q=['height_cm__to_value__gte'], gt=0)
    height_cm_to_lte: int = Field(None, q=['height_cm__to_value__lte'], gt=0)

    years_to_max_height_from_gte: int = Field(None, q=['years_to_max_height__from_value__gte'], gt=0)
    years_to_max_height_from_lte: int = Field(None, q=['years_to_max_height__from_value__lte'], gt=0)
    years_to_max_height_to_gte: int = Field(None, q=['years_to_max_height__to_value__gte'], gt=0)
    years_to_max_height_to_lte: int = Field(None, q=['years_to_max_height__to_value__lte'], gt=0)

    spread_cm_from_gte: int = Field(None, q=['spread_cm__from_value__gte'], gt=0)
    spread_cm_from_lte: int = Field(None, q=['spread_cm__from_value__lte'], gt=0)
    spread_cm_to_gte: int = Field(None, q=['spread_cm__to_value__gte'], gt=0)
    spread_cm_to_lte: int = Field(None, q=['spread_cm__to_value__lte'], gt=0)

    def _resolve_field_expression(self, field_name: str, field_value: t.Any, field: FieldInfo) -> Q:
        if field_name in BIT_FIELD_VALUES and field_value:
            return self._filter_bit_field(field_name, field_value)
        return super()._resolve_field_expression(field_name, field_value, field)

    @staticmethod
    def _filter_bit_field(field_name: str, choices: list[TextChoices]) -> Q:
        q = Q()

        if not (model_field := getattr(Specie, field_name, None)):
            return q

        for choice in choices:
            if bit_flag := getattr(model_field, choice.value, None):
                q &= Q(**{field_name: bit_flag})
        return q
