from enum import Enum

from bitfield import BitField
from django.db import models
from django.utils.text import slugify


class Specie(models.Model):
    class SoilPhChoices(models.TextChoices):
        ACID = ('acid', 'Acid')
        NEUTRAL = ('neutral', 'Neutral')
        ALKALINE = ('alkaline', 'Alkaline')

    class SoilTypeChoices(models.TextChoices):
        CLAY = ('clay', 'Clay')
        SAND = ('sand', 'Sand')
        CHALK = ('chalk', 'Chalk')
        LOAM = ('loam', 'Loam')

    class SoilMoistureChoices(models.TextChoices):
        MOIST_WELL_DRAINED = ('moist_well_drained', 'Moist but well-drained')
        POORLY_DRAINED = ('poorly_drained', 'Poorly-drained')
        WELL_DRAINED = ('well_drained', 'Well-drained')

    class DurationChoices(models.TextChoices):
        ANNUAL = ('annual', 'Annual')
        BIENNIAL = ('biennial', 'Biennial')
        PERENNIAL = ('perennial', 'Perennial')

    class PlantPartsChoices(models.TextChoices):
        BARK = ('bark', 'Bark')
        FRUIT = ('fruit', 'Fruit')
        FLOWER = ('flower', 'Flower')
        HABIT = ('habit', 'Habit')
        LEAF = ('leaf', 'Leaf')
        OTHER = ('other', 'Other')
        ROOT = ('root', 'Root')
        STEM = ('stem', 'Stem')
        SEED = ('seed', 'Seed')
        TUBER = ('tuber', 'Tuber')
        FOLIAGE = ('foliage', 'Foliage')

    class PositionSunlightChoices(models.TextChoices):
        PARTIAL_SHADE = ('partial_shade', 'Partial shade')
        FULL_SUN = ('full_sun', 'Full sun')
        FULL_SHADE = ('full_shade', 'Full shade')

    class PositionSideChoices(models.TextChoices):
        EAST_FACING = ('east_facing', 'East-facing')
        NORTH_FACING = ('north_facing', 'North-facing')
        WEST_FACING = ('west_facing', 'West-facing')
        SOUTH_FACING = ('south_facing', 'South-facing')

    class SeasonsChoices(models.TextChoices):
        SPRING = ('spring', 'Spring')
        SUMMER = ('summer', 'Summer')
        AUTUMN = ('autumn', 'Autumn')
        WINTER = ('winter', 'Winter')

    class ToxicTypesChoices(models.TextChoices):
        TOXIC_TO_CATS = ('toxic_to_cats', 'Toxic to Cats')
        SLIGHTLY_TOXIC_TO_HUMANS = ('slightly_toxic_to_humans', 'Slightly Toxic to Humans')
        MODERATE_TOXIC_TO_HUMANS = ('moderate_toxic_to_humans', 'Moderate Toxic to Humans')
        HIGHLY_TOXIC_TO_HUMANS = ('highly_toxic_to_humans', 'Highly Toxic to Humans')
        TOXIC_TO_DOGS = ('toxic_to_dogs', 'Toxic to Dogs')

    class FoliageTypesChoices(models.TextChoices):
        DECIDUOUS = ('deciduous', 'Deciduous')
        EVERGREEN = ('evergreen', 'Evergreen')
        SEMI_EVERGREEN = ('semi_evergreen', 'Semi evergreen')

    class HabitTypesChoices(models.TextChoices):
        TUFTED = ('tufted', 'Tufted')
        TRAILING = ('trailing', 'Trailing')
        PENDULOUS_WEEPING = ('pendulous_weeping', 'Pendulous weeping')
        CLUMP_FORMING = ('clump_forming', 'Clump forming')
        COLUMNAR_UPRIGHT = ('columnar_upright', 'Columnar upright')
        SUBMERGED = ('submerged', 'Submerged')
        SUCKERING = ('suckering', 'Suckering')
        FLOATING = ('floating', 'Floating')
        MAT_FORMING = ('mat_forming', 'Matforming')
        BUSHY = ('bushy', 'Bushy')
        CLIMBING = ('climbing', 'Climbing')

    class ExposureChoices(models.TextChoices):
        EXPOSED = ('exposed', 'Exposed')
        SHELTERED = ('sheltered', 'Sheltered')
        EXPOSED_OR_SHELTERED = ('exposed_or_sheltered', 'Exposed or Sheltered')
        SHELTERED_OR_EXPOSED = ('sheltered_or_exposed', 'Sheltered or Exposed')

    class SeasonsMaxChoices(models.TextChoices):
        WINTER = ('winter', 'Winter')
        SPRING = ('spring', 'Spring')
        MID_AUTUMN = ('mid_autumn', 'Mid autumn')
        MID_SUMMER = ('mid_summer', 'Mid summer')
        SUMMER = ('summer', 'Summer')
        AUTUMN = ('autumn', 'Autumn')
        LATE_AUTUMN = ('late_autumn', 'Late autumn')
        ALL_YEAR_AROUND = ('all_year_around', 'All year around')
        MID_SPRING = ('mid_spring', 'Mid spring')
        MID_WINTER = ('mid_winter', 'Mid winter')
        LATE_SUMMER = ('late_summer', 'Late summer')
        EARLY_AUTUMN = ('early_autumn', 'Early autumn')
        LATE_WINTER = ('late_winter', 'Late winter')
        EARLY_SUMMER = ('early_summer', 'Early summer')
        LATE_SPRING = ('late_spring', 'Late spring')
        EARLY_SPRING = ('early_spring', 'Early spring')
        EARLY_WINTER = ('early_winter', 'Early winter')

    slug = models.SlugField(max_length=256, unique=True)
    image_url = models.URLField(null=True, blank=True)
    latin_name = models.CharField(max_length=256, db_index=True, unique=True)
    genus_description = models.TextField(default='', blank=True)

    duration = models.CharField(
        null=True,
        max_length=64,
        choices=DurationChoices.choices,
        help_text='BitFlag. How long does the plant live in time.',
    )
    edible = models.BooleanField(
        null=True,
        db_index=True,
        help_text='Is the species edible?',
    )
    edible_part = BitField(
        null=True,
        flags=PlantPartsChoices.choices,
        db_index=True,
        help_text='BitFlag. The plant edible part(s), if any.',
    )

    rating = models.PositiveIntegerField(
        default=9999999,
        db_index=True,
        help_text='How popular is our plant among others in the database.',
    )

    height_cm = models.OneToOneField(
        'IntervalValue',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='height_cm',
    )
    years_to_max_height = models.OneToOneField(
        'IntervalValue',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='years_to_max_height',
    )
    spread_cm = models.OneToOneField(
        'IntervalValue',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='spread_cm',
    )

    soil_type = BitField(
        null=True,
        flags=SoilTypeChoices.choices,
        db_index=True,
        help_text='BitFlag. The type of soil in which the plant can grow.',
    )
    soil_moisture = BitField(
        null=True,
        flags=SoilMoistureChoices.choices,
        db_index=True,
        help_text='BitFlag. Ground humidity level.',
    )
    soil_ph = BitField(
        null=True,
        flags=SoilPhChoices.choices,
        db_index=True,
        help_text='BitFlag. The acidity of the soil required for the plant.',
    )

    position_sunlight = BitField(
        null=True,
        flags=PositionSunlightChoices.choices,
        db_index=True,
        help_text='BitFlag. The level of sunlight on the plant.',
    )
    position_side = BitField(
        null=True,
        flags=PositionSideChoices.choices,
        db_index=True,
        help_text='BitFlag. The side of the world where the plant can grow well.',
    )
    exposure = models.CharField(
        null=True,
        max_length=64,
        choices=ExposureChoices.choices,
        db_index=True,
        help_text='Sun-loving or not plant. The amount of light that the plant receives.',
    )

    hardiness_zone = models.CharField(default='', max_length=4, blank=True)
    fragrance = BitField(
        null=True,
        flags=PlantPartsChoices.choices,
        db_index=True,
        help_text='Which part of the plant emits fragrance.',
    )
    cultivation = models.TextField(default='', blank=True, help_text='cultivation tips.')
    harvest = BitField(
        null=True,
        flags=SeasonsMaxChoices.choices,
        db_index=True,
        help_text='BitFlag. The time at which to harvest, if any.',
    )
    planting = BitField(
        null=True,
        flags=SeasonsMaxChoices.choices,
        db_index=True,
        help_text='BitFlag. The time at which to plant the plant.',
    )

    toxicity = BitField(
        null=True,
        flags=ToxicTypesChoices.choices,
        db_index=True,
        help_text='BitFlag. The level of toxicity of the plant to humans and animals.',
    )

    foliage = BitField(
        null=True,
        flags=FoliageTypesChoices.choices,
        db_index=True,
        help_text='BitFlag. Features regarding seasonal changes in foliage.',
    )
    habit = BitField(
        null=True,
        flags=HabitTypesChoices.choices,
        db_index=True,
        help_text='BitFlag. '
                  'The general shape and morphology of the plant, its growth method and organization of structures.',
    )

    scientific_classification = models.OneToOneField(
        'ScientificClassification',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    misc = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.latin_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.latin_name


# There are duplicates by name for one plant, they need to be removed and added accordingly. constrain
class CommonName(models.Model):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='common_names')
    lang = models.CharField(max_length=8)
    name = models.CharField(max_length=256, db_index=True, unique=True)
    is_main = models.BooleanField(default=False, help_text='Is this the main name for the species?')

    def __str__(self):
        return f'{self.name}::{self.lang} (is_main={self.is_main})'


# There are duplicates by name for one plant, they need to be removed and added accordingly. constrain
class Synonym(models.Model):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='synonyms')
    name = models.CharField(max_length=256, db_index=True, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    specie = models.ManyToManyField(Specie, related_name='tags')
    name = models.CharField(max_length=256, db_index=True, unique=True)

    def __str__(self):
        return self.name


class PartColor(models.Model):
    class SeasonsLiteChoices(models.TextChoices):
        SPRING = ('spring', 'Spring')
        SUMMER = ('summer', 'Summer')
        AUTUMN = ('autumn', 'Autumn')
        WINTER = ('winter', 'Winter')

    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='parts_color')
    plant_part = models.CharField(max_length=64, choices=Specie.PlantPartsChoices.choices)
    season = models.CharField(max_length=64, choices=SeasonsLiteChoices.choices)

    def __str__(self):
        return self.get_plant_part_display()


class Color(models.Model):
    color = models.ManyToManyField(PartColor, related_name='colors_part')
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    image_copyright = models.CharField(max_length=512)
    part = models.CharField(
        max_length=64,
        choices=Specie.PlantPartsChoices.choices,
        help_text='Which part of the plant is this photo?',
    )

    def __str__(self):
        return self.image_url


class Source(models.Model):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='sources')
    last_update = models.DateTimeField()
    sid = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    source_url = models.URLField(null=True, blank=True)
    citation = models.CharField(default='', blank=True, max_length=256)

    def __str__(self):
        return self.name


class IntervalValue(models.Model):
    from_value = models.PositiveIntegerField(null=True)
    to_value = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'from {self.from_value} to {self.to_value}'


class RegularEvent(models.Model):
    class TimePartChoices(models.TextChoices):
        MINUTE = ('minute', 'Minute')
        HOUR = ('hour', 'Hour')
        DAY = ('day', 'Day')
        WEEK = ('week', 'Week')
        FORTNIGHT = ('fortnight', 'Fortnight')
        MONTH = ('month', 'Month')
        YEAR = ('year', 'Year')
        CENTURY = ('century', 'Century')

    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='regular_events')
    name = models.CharField(max_length=256)
    frequency = models.OneToOneField(IntervalValue, on_delete=models.CASCADE)
    frequency_count = models.PositiveSmallIntegerField(default=1)
    frequency_unit = models.CharField(max_length=64, choices=TimePartChoices.choices)

    class Meta:
        unique_together = ('specie', 'name')

    def __str__(self):
        return f'{self.name} {self.frequency_count}*{self.get_frequency_unit_display()}'


class ScientificClassification(models.Model):
    family = models.CharField(default='', blank=True, max_length=128)
    phylum = models.CharField(default='', blank=True, max_length=128)
    classify = models.CharField(default='', blank=True, max_length=128)
    genus = models.CharField(default='', blank=True, max_length=128)
    species = models.CharField(default='', blank=True, max_length=128)


class Order(models.Model):
    scientific_classification = models.ForeignKey(
        'ScientificClassification',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    name = models.CharField(default='', blank=True, max_length=256)

    def __str__(self):
        return self.name


class BasePlantSpecification(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Pathogen(BasePlantSpecification):
    class PathogenTypesChoices(models.TextChoices):
        DISEASE = ('disease', 'Disease')
        PEST = ('pest', 'Pest')

    specie = models.ManyToManyField(Specie, related_name='pathogens')
    pathogen_type = models.CharField(
        max_length=64,
        choices=PathogenTypesChoices.choices,
    )

    def __str__(self):
        return f'{self.name}: {self.get_pathogen_type_display()}'


class Distribution(BasePlantSpecification):
    specie = models.ManyToManyField(Specie, through='DistributionSpecie')

    tdwg_code = models.CharField(default='', blank=True, max_length=16)
    tdwg_level = models.PositiveIntegerField()
    species_count = models.PositiveIntegerField()

    def __str__(self):
        return self.tdwg_code


class DistributionSpecie(models.Model):
    class DistributionTypesChoices(models.TextChoices):
        NATIVE = ('native', 'Native')
        INTRODUCED = ('introduced', 'Introduced')
        DOUBTFUL = ('doubtful', 'Doubtful')
        ABSENT = ('absent', 'Absent')
        EXTINCT = ('extinct', 'Extinct')

    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='distributions_specie')
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE)
    statuses = BitField(
        null=True,
        flags=DistributionTypesChoices.choices,
        help_text='BitFlag. DistributionSpecie.',
    )


class GrowthTip(BasePlantSpecification):
    class GrowthTipChoices(models.TextChoices):
        PROPAGATION = ('propagation', 'Propagation')
        SUGGESTED_PLANTING_PLACES = ('suggested_panting_places', 'Suggested Planting Places')
        PRUNING = ('pruning', 'Pruning')

    specie = models.ManyToManyField(Specie, related_name='growth_tips')
    tip_type = models.CharField(max_length=64, choices=GrowthTipChoices.choices)

    def __str__(self):
        return f'{self.name}: {self.get_tip_type_display()}'
