import typing as t
from collections import defaultdict

import annotated_types
from ninja import Field, ModelSchema, Schema
from pydantic import create_model as create_pydantic_model
from typing_extensions import Annotated

from qt_search.models import (
    CommonName,
    DistributionSpecie,
    GrowthTip,
    Image,
    IntervalValue,
    PartColor,
    Pathogen,
    RegularEvent,
    ScientificClassification,
    Source,
    Specie,
)

LimitStr = Annotated[str, annotated_types.MaxLen(256)]
LangStr = Annotated[str, annotated_types.MaxLen(8)]


class IDValueSchema(Schema):
    value: str
    label: str


class ExposureSchema(IDValueSchema):
    value: Specie.ExposureChoices


class DurationSchema(IDValueSchema):
    value: Specie.DurationChoices


class SoilTypeSchema(IDValueSchema):
    value: Specie.SoilTypeChoices


class SoilMoistureSchema(IDValueSchema):
    value: Specie.SoilMoistureChoices


class SoilPhSchema(IDValueSchema):
    value: Specie.SoilPhChoices


class PositionSunlightSchema(IDValueSchema):
    value: Specie.PositionSunlightChoices


class PositionSideSchema(IDValueSchema):
    value: Specie.PositionSideChoices


class PlantPartsSchema(IDValueSchema):
    value: Specie.PlantPartsChoices


class SeasonsMaxSchema(IDValueSchema):
    value: Specie.SeasonsMaxChoices


class ToxicitySchema(IDValueSchema):
    value: Specie.ToxicTypesChoices


class FoliageSchema(IDValueSchema):
    value: Specie.FoliageTypesChoices


class HabitSchema(IDValueSchema):
    value: Specie.HabitTypesChoices


class DistributionsSchema(IDValueSchema):
    value: DistributionSpecie.DistributionTypesChoices


class SeasonsLiteSchema(IDValueSchema):
    value: PartColor.SeasonsLiteChoices


class TimePartSchema(IDValueSchema):
    value: RegularEvent.TimePartChoices


class ScientificClassificationSchema(ModelSchema):
    orders: list[LimitStr]

    class Meta:
        model = ScientificClassification
        fields = ('family', 'phylum', 'classify', 'genus', 'species')

    @staticmethod
    def resolve_orders(obj) -> list[LimitStr]:
        return [order.name for order in obj.orders.all()]


class IntervalValueSchema(ModelSchema):
    class Meta:
        model = IntervalValue
        fields = ('from_value', 'to_value')


class SourcesSchema(ModelSchema):
    class Meta:
        model = Source
        exclude = ('id', 'specie')


class CommonNamesSchema(ModelSchema):
    class Meta:
        model = CommonName
        fields = ('name', 'lang')

    @staticmethod
    def resolve_name(obj):
        return obj.name.capitalize()


class ImageItemSchema(ModelSchema):
    class Meta:
        model = Image
        fields = ('image_url', 'image_copyright')


GroupedImagesSchema = create_pydantic_model(
    'GroupedImagesSchema',
    **{part: (list[ImageItemSchema], []) for part in Specie.PlantPartsChoices.values},
)


class PathogenItemSchema(ModelSchema):
    pathogen_type: str = Field(..., alias='get_pathogen_type_display')

    class Meta:
        model = Pathogen
        fields = 'name',


GroupedPathogensSchema = create_pydantic_model(
    'GroupedPathogensSchema',
    **{pathogen: (list[LimitStr], []) for pathogen in Pathogen.PathogenTypesChoices.values},
)


class GrowthTipItemSchema(ModelSchema):
    tip_type: str = Field(..., alias='get_tip_type_display')

    class Meta:
        model = GrowthTip
        fields = 'name',


GroupedGrowthTipsSchema = create_pydantic_model(
    'GrowthTipsSchema',
    **{tip: (list[LimitStr], []) for tip in GrowthTip.GrowthTipChoices.values},
)


class PartColorItemSchema(Schema):
    plant_part_: str = Field('other', alias='get_plant_part_display', exclude=True)
    season: SeasonsLiteSchema
    colors: list[LimitStr]

    @staticmethod
    def resolve_season(obj) -> SeasonsLiteSchema | None:
        if season := obj.season:
            return SeasonsLiteSchema(value=season, label=obj.get_season_display())
        return None

    @staticmethod
    def resolve_colors(obj) -> list[LimitStr]:
        return [part.name for part in obj.colors_part.all()]


GroupedPartColorsSchema = create_pydantic_model(
    'GroupedPartColorsSchema',
    **{part: (list[PartColorItemSchema], []) for part in Specie.PlantPartsChoices.values},
)


class RegularEventItemSchema(ModelSchema):
    frequency: IntervalValueSchema
    frequency_unit: TimePartSchema

    @staticmethod
    def resolve_frequency_unit(obj) -> TimePartSchema:
        return TimePartSchema(value=obj.frequency_unit, label=obj.get_frequency_unit_display())

    class Meta:
        model = RegularEvent
        fields = ('name', 'frequency', 'frequency_count', 'frequency_unit')


class DistributionItemSchema(Schema):
    statuses: list[DistributionsSchema] = Field(..., alias='statuses.get_set_data')
    name: str = Field(..., max_length=256, alias='distribution.name')
    tdwg_code: str = Field(..., max_length=16, alias='distribution.tdwg_code')
    tdwg_level: int = Field(..., alias='distribution.tdwg_level')
    species_count: int = Field(..., alias='distribution.species_count')


class SpeciesSchema(ModelSchema):
    main_common_name: LimitStr | None

    class Meta:
        model = Specie
        fields = ('slug', 'latin_name', 'image_url')

    @staticmethod
    def resolve_main_common_name(obj: Specie) -> LimitStr | None:
        if main_common_name := next(iter(obj.main_common_name or []), None):
            return main_common_name.name
        return None


class SpeciesDetailsSchema(ModelSchema):
    main_common_name: LimitStr | None
    tags: list[LimitStr]
    synonyms: list[LimitStr]
    sources: list[SourcesSchema]

    common_names: t.DefaultDict[LangStr, list[LimitStr]]
    images: GroupedImagesSchema
    pathogens: GroupedPathogensSchema
    growth_tips: GroupedGrowthTipsSchema
    distributions: list[DistributionItemSchema] = Field(..., alias='distributions_specie')
    regular_events: list[RegularEventItemSchema]
    parts_color: GroupedPartColorsSchema

    exposure: ExposureSchema | None = None
    duration: DurationSchema | None = None

    edible_part: list[PlantPartsSchema] = Field([], alias='edible_part.get_set_data')
    soil_type: list[SoilTypeSchema] = Field([], alias='soil_type.get_set_data')
    soil_moisture: list[SoilMoistureSchema] = Field([], alias='soil_moisture.get_set_data')
    soil_ph: list[SoilPhSchema] = Field([], alias='soil_ph.get_set_data')
    position_sunlight: list[PositionSunlightSchema] = Field([], alias='position_sunlight.get_set_data')
    position_side: list[PositionSideSchema] = Field([], alias='position_side.get_set_data')
    fragrance: list[PlantPartsSchema] = Field([], alias='fragrance.get_set_data')
    harvest: list[SeasonsMaxSchema] = Field([], alias='harvest.get_set_data')
    planting: list[SeasonsMaxSchema] = Field([], alias='planting.get_set_data')
    toxicity: list[ToxicitySchema] = Field([], alias='toxicity.get_set_data')
    foliage: list[FoliageSchema] = Field([], alias='foliage.get_set_data')
    habit: list[HabitSchema] = Field([], alias='habit.get_set_data')

    height_cm: IntervalValueSchema | None
    years_to_max_height: IntervalValueSchema | None
    spread_cm: IntervalValueSchema | None

    scientific_classification: ScientificClassificationSchema | None

    class Meta:
        model = Specie
        fields = (
            'slug',
            'latin_name',
            'image_url',
            'genus_description',
            'edible',
            'rating',
            'cultivation',
            'created',
            'modified',
            'misc'
        )

    @staticmethod
    def resolve_exposure(obj) -> ExposureSchema | None:
        if exposure := obj.exposure:
            return ExposureSchema(value=exposure, label=obj.get_exposure_display())
        return None

    @staticmethod
    def resolve_duration(obj) -> DurationSchema | None:
        if duration := obj.duration:
            return DurationSchema(value=duration, label=obj.get_duration_display())
        return None

    @staticmethod
    def resolve_tags(obj) -> list[LimitStr]:
        return [tag.name for tag in obj.tags.all()]

    @staticmethod
    def resolve_synonyms(obj) -> list[LimitStr]:
        return [synonym.name for synonym in obj.synonyms.all()]

    @staticmethod
    def resolve_common_names(obj) -> t.DefaultDict[LangStr, list[LimitStr]]:
        grouped_data: t.DefaultDict[LangStr, list[LimitStr]] = defaultdict(list)
        for common_name in obj.common_names.all():
            name: str = common_name.name
            grouped_data[common_name.lang].append(name.capitalize())
        return grouped_data

    @staticmethod
    def resolve_images(obj) -> GroupedImagesSchema:
        grouped_data: t.DefaultDict[str, list[Image]] = defaultdict(list)
        for item in obj.images.all():
            if not (plant_part := item.part) or plant_part not in Specie.PlantPartsChoices.values:
                raise ValueError("'plant_part' not founded")
            grouped_data[plant_part].append(item)
        return GroupedImagesSchema(**grouped_data)

    @staticmethod
    def resolve_pathogens(obj) -> GroupedPathogensSchema:
        grouped_data: t.DefaultDict[str, list[LimitStr]] = defaultdict(list)
        for item in obj.pathogens.all():
            grouped_data[item.pathogen_type].append(item.name)
        return GroupedPathogensSchema(**grouped_data)

    @staticmethod
    def resolve_growth_tips(obj) -> GroupedGrowthTipsSchema:
        grouped_data: t.DefaultDict[str, list[LimitStr]] = defaultdict(list)
        for item in obj.growth_tips.all():
            grouped_data[item.tip_type].append(item.name)
        return GroupedGrowthTipsSchema(**grouped_data)

    @staticmethod
    def resolve_parts_color(obj) -> GroupedPartColorsSchema:
        grouped_data: t.DefaultDict[str, list[PartColorItemSchema]] = defaultdict(list)
        for item in obj.parts_color.all():
            if not (plant_part := item.plant_part) or plant_part not in Specie.PlantPartsChoices.values:
                raise ValueError("'plant_part' not founded")
            grouped_data[plant_part].append(item)
        return GroupedPartColorsSchema(**grouped_data)

    @staticmethod
    def resolve_main_common_name(obj: Specie) -> LimitStr | None:
        if main_common_name := next(iter(obj.main_common_name or []), None):
            return main_common_name.name
        return None
