import typing as t

from pydantic import BaseModel, Field, ValidationError, create_model, field_validator, model_validator

from common import typing as cust_t
from qt_search.models import DistributionSpecie, Specie


class IntervalValueModel(BaseModel):
    from_value: int | None = Field(None, gt=0)
    to_value: int | None = Field(None, gt=0)

    @model_validator(mode='after')
    @classmethod
    def check_all_is_none(cls, data):
        if all(not v for k, v in data):
            return None
        return data


class SizeModel(BaseModel):
    height_cm: IntervalValueModel | None = None
    years_to_max_height: IntervalValueModel | None = None
    spread_cm: IntervalValueModel | None = None

    @field_validator('height_cm', 'years_to_max_height', 'spread_cm', mode='before')
    @classmethod
    def size_contain_value(cls, value) -> IntervalValueModel | None:
        try:
            return IntervalValueModel(**value)
        except (ValidationError, TypeError):
            return None


class WaterModel(BaseModel):
    frequency: IntervalValueModel | None
    frequency_count: int
    frequency_unit: str

    @field_validator('frequency', mode='before')
    @classmethod
    def frequency_contain_value(cls, value) -> IntervalValueModel | None:
        try:
            return IntervalValueModel(**value)
        except (ValidationError, TypeError):
            return None


class SoilModel(BaseModel):
    water: WaterModel | None = None
    type: list[cust_t.SoilType] = []  # noqa: A003
    moisture: list[cust_t.SoilMoisture] = []
    ph: list[cust_t.SoilPh] = []

    @field_validator('water', mode='before')
    @classmethod
    def set_water_none(cls, value) -> WaterModel | None:
        try:
            return WaterModel(**value)
        except (ValidationError, TypeError):
            return None


class PositionModel(BaseModel):
    sunlight: list[cust_t.PositionSunlight] = []
    side: list[cust_t.PositionSide] = []
    exposure: cust_t.Exposure | None = None
    hardiness_zone: str | None = ''


class EventsModel(BaseModel):
    harvest: list[cust_t.SeasonsMax] = []
    planting: list[cust_t.SeasonsMax] = []


class ColorModel(BaseModel):
    stem: list[str] = []
    flower: list[str] = []
    foliage: list[str] = []
    fruit: list[str] = []


class ColourAndScentModel(BaseModel):
    fragrance: list[cust_t.PlantParts] | None = []
    spring: ColorModel = ColorModel()
    summer: ColorModel = ColorModel()
    autumn: ColorModel = ColorModel()
    winter: ColorModel = ColorModel()


class HowToGrowModel(BaseModel):
    cultivation: str | None = ''
    propagation: list[str] = []
    suggested_panting_places: list[str] = []
    pruning: list[str] = []


class ScientificClassificationModel(BaseModel):
    family: str | None
    phylum: str | None
    classify: str | None
    order: list[str]
    genus: str | None
    species: str | None

    @model_validator(mode='after')
    @classmethod
    def check_all_is_none(cls, data):
        if all(not v for k, v in data):
            return None
        return data


class BotanicalDetailsModel(BaseModel):
    foliage: list[cust_t.FoliageTypes] = []
    habit: list[cust_t.HabitTypes] = []


class ImageSourceModel(BaseModel):
    image_url: str
    copyright: str  # noqa: A003


class DistributionSourceModel(BaseModel):
    name: str
    tdwg_code: str
    tdwg_level: int
    species_count: int


DynamicImagesModel = create_model(
    'ImagesModel',
    **{part.lower(): (list[ImageSourceModel], []) for part in Specie.PlantPartsChoices.values},
)

DynamicDistributionModel = create_model(
    'DistributionModel',
    **{dist: (list[DistributionSourceModel], []) for dist in DistributionSpecie.DistributionTypesChoices.values}
)


class SourceModel(BaseModel):
    last_update: str
    id: str  # noqa: A003
    name: str
    url: str | None
    citation: str | None = ""


class SpeciesModel(BaseModel):
    latin_name: str
    main_common_name: dict[str, str] = {}
    common_names: dict[str, list[str]] = {}
    image_url: str | None = None
    images: DynamicImagesModel = DynamicImagesModel()
    duration: cust_t.Duration | None = None
    edible: bool | None = None
    edible_part: list[cust_t.PlantParts] = []
    synonyms: list[str] = []
    tags: list[str] = []
    genus_description: str | None = ""
    rank: int = 999999
    size: SizeModel = SizeModel()
    soil: SoilModel = SoilModel()
    position: PositionModel = PositionModel()
    events: EventsModel = EventsModel()
    colour_and_scent: ColourAndScentModel = ColourAndScentModel()
    toxicity: list[cust_t.ToxicTypes] = []
    how_to_grow: HowToGrowModel = HowToGrowModel()
    diseases_and_pests: list[str] = []
    scientific_classification: ScientificClassificationModel | None = None
    botanical_details: BotanicalDetailsModel = BotanicalDetailsModel()
    distributions: DynamicDistributionModel = DynamicDistributionModel()
    sources: list[SourceModel] = []
    misc: dict[str, t.Any] = {}

    @field_validator('genus_description', mode='after')
    @classmethod
    def set_water_none(cls, value) -> str:
        return value or ""
