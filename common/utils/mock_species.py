from django.db.utils import IntegrityError

from common.models import SpeciesModel
from qt_search.models import (
    Color,
    CommonName,
    Distribution,
    DistributionSpecie,
    GrowthTip,
    Image,
    IntervalValue,
    Order,
    PartColor,
    Pathogen,
    RegularEvent,
    ScientificClassification,
    Source,
    Specie,
    Synonym,
    Tag,
)

part_choice_dict = dict(Specie.PlantPartsChoices.choices)
season_choice_dict = dict(PartColor.SeasonsLiteChoices.choices)
growth_tips_dict = dict(GrowthTip.GrowthTipChoices.choices)

exposure_choice_dict = dict(zip(Specie.ExposureChoices.labels, Specie.ExposureChoices.values))
duration_choice_dict = dict(zip(Specie.DurationChoices.labels, Specie.DurationChoices.values))


def get_bit_flag(flags, mask):
    if not flags:
        return None

    new_value = 0
    for bit_number, label in enumerate(mask):
        if label in flags:
            new_value |= 2 ** bit_number
    return new_value


def create_db_specie(sp: SpeciesModel):  # noqa: C901
    try:
        specie = Specie.objects.create(
            image_url=sp.image_url,
            latin_name=sp.latin_name,
            genus_description=sp.genus_description,
            soil_type=get_bit_flag(sp.soil.type, Specie.SoilTypeChoices.labels),
            duration=duration_choice_dict.get(sp.duration),
            edible=sp.edible,
            edible_part=get_bit_flag(sp.edible_part, Specie.PlantPartsChoices.labels),
            rating=sp.rank,
            soil_moisture=get_bit_flag(sp.soil.moisture, Specie.SoilMoistureChoices.labels),
            soil_ph=get_bit_flag(sp.soil.ph, Specie.SoilPhChoices.labels),
            position_sunlight=get_bit_flag(sp.position.sunlight, Specie.PositionSunlightChoices.labels),
            position_side=get_bit_flag(sp.position.side, Specie.PositionSideChoices.labels),
            exposure=exposure_choice_dict.get(sp.position.exposure),
            hardiness_zone=sp.position.hardiness_zone,
            fragrance=get_bit_flag(sp.colour_and_scent.fragrance, Specie.PlantPartsChoices.labels),
            cultivation=sp.how_to_grow.cultivation,
            harvest=get_bit_flag(sp.events.harvest, Specie.SeasonsMaxChoices.labels),
            planting=get_bit_flag(sp.events.planting, Specie.SeasonsMaxChoices.labels),
            toxicity=get_bit_flag(sp.toxicity, Specie.ToxicTypesChoices.labels),
            foliage=get_bit_flag(sp.botanical_details.foliage, Specie.FoliageTypesChoices.labels),
            habit=get_bit_flag(sp.botanical_details.habit, Specie.HabitTypesChoices.labels),
            misc=sp.misc,
        )
    except IntegrityError:
        return

    if height_cm := sp.size.height_cm:
        specie.height_cm = IntervalValue.objects.create(**height_cm.model_dump())

    if years_to_max_height := sp.size.years_to_max_height:
        specie.years_to_max_height = IntervalValue.objects.create(**years_to_max_height.model_dump())

    if spread_cm := sp.size.spread_cm:
        specie.spread_cm = IntervalValue.objects.create(**spread_cm.model_dump())

    if sclass := sp.scientific_classification:
        sclass_obj = ScientificClassification.objects.create(
            family=sclass.family or "",
            phylum=sclass.phylum or "",
            classify=sclass.classify or "",
            genus=sclass.genus or "",
            species=sclass.species or "",
        )
        Order.objects.bulk_create([
            Order(scientific_classification=sclass_obj, name=order) for order in sclass.order
        ])
        specie.scientific_classification = sclass_obj

    specie.save(update_fields=["height_cm", "years_to_max_height", "spread_cm", "scientific_classification"])

    # Нужно сделать балком, а то не очень как-то
    for lang, mcommon_name in sp.main_common_name.items():
        try:
            CommonName.objects.get(name=mcommon_name)
        except CommonName.DoesNotExist:
            CommonName(specie=specie, name=mcommon_name, lang=lang, is_main=True).save()

    for lang, common_names in sp.common_names.items():
        for name in common_names:
            try:
                CommonName.objects.get(name=name)
            except CommonName.DoesNotExist:
                CommonName(specie=specie, name=name, lang=lang, is_main=False).save()

    for synonym in sp.synonyms:
        try:
            Synonym.objects.get(name=synonym)
        except Synonym.DoesNotExist:
            Synonym(specie=specie, name=synonym).save()

    specie.tags.set([Tag.objects.get_or_create(name=tag)[0] for tag in sp.tags])

    bulk_images = []
    for plant_part, images in sp.images:
        bulk_images.extend([
            Image(
                specie=specie,
                image_url=image.image_url,
                image_copyright=image.copyright,
                part=plant_part
            ) for image in images
        ])
    Image.objects.bulk_create(bulk_images)

    Source.objects.bulk_create([
        Source(
            specie=specie,
            last_update=source.last_update,
            sid=source.id,
            name=source.name,
            source_url=source.url,
            citation=source.citation or "",
        ) for source in sp.sources
    ])

    if water := sp.soil.water:
        frequency = IntervalValue.objects.create(**water.frequency.model_dump())
        RegularEvent.objects.create(
            specie=specie,
            name="water",
            frequency=frequency,
            frequency_count=water.frequency_count,
            frequency_unit=water.frequency_unit,
        )

    specie.pathogens.set([
        Pathogen.objects.get_or_create(
            name=ptg, defaults={'pathogen_type': 'disease'}
        )[0] for ptg in sp.diseases_and_pests
    ])

    for distribution_type, distributions in sp.distributions:
        for distribution in distributions:
            distribution, created = Distribution.objects.get_or_create(
                name=distribution.name,
                tdwg_code=distribution.tdwg_code,
                tdwg_level=distribution.tdwg_level,
                species_count=distribution.species_count,
            )
            DistributionSpecie.objects.create(
                specie=specie,
                distribution=distribution,
                statuses=get_bit_flag(distribution_type, DistributionSpecie.DistributionTypesChoices.values),
            )

    bulk_growth_tips = []
    for growth_tips_type, growth_tips in sp.how_to_grow:
        if growth_tips_type == "cultivation":
            continue
        for growth_tip in growth_tips:
            obj, _ = GrowthTip.objects.get_or_create(
                name=growth_tip, defaults={'tip_type': growth_tips_type}
            )
            bulk_growth_tips.append(obj)
    specie.growth_tips.set(bulk_growth_tips)

    for s_name, colors_by_season in sp.colour_and_scent:
        if s_name == 'fragrance':
            continue
        for part, colors in colors_by_season:
            if not colors:
                continue
            pc = PartColor.objects.create(
                specie=specie, plant_part=part, season=s_name
            )
            pc.colors_part.set([Color.objects.get_or_create(name=color)[0] for color in colors])
