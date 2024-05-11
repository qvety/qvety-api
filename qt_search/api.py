from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.pagination import PageNumberPagination, paginate
from ninja.params import Query

from qt_search.models import CommonName, DistributionSpecie, Specie
from qt_search.schemas.filter import FiltersSchema
from qt_search.schemas.specie import SpeciesDetailsSchema, SpeciesSchema

app = NinjaAPI()


@app.get("/species/", response=list[SpeciesSchema])
@paginate(PageNumberPagination)
def get_species(request, filters: FiltersSchema = Query(...)):    # noqa: B008
    species = filters.filter(
        Specie.objects
        .prefetch_related(
            Prefetch(
                'common_names',
                queryset=CommonName.objects.filter(is_main=True, lang='en')[:1],
                to_attr='main_common_name',
            )).only('slug', 'latin_name', 'image_url').order_by('rating').all()
    )
    return species


@app.get("/species/{slug}/", response=SpeciesDetailsSchema)
def get_specie_details(request, slug: str):
    return get_object_or_404(
        Specie.objects.prefetch_related(
            'tags',
            Prefetch(
                'common_names',
                queryset=CommonName.objects.filter(is_main=True, lang='en'),
                to_attr='main_common_name',
            ),
            Prefetch(
                'distributions_specie',
                queryset=DistributionSpecie.objects.select_related('distribution'),
            ),
            'tags',
            'parts_color__colors_part',
            'synonyms',
            'growth_tips',
            'regular_events',
            'parts_color',
            'images',
            'sources',
            'pathogens',
        ).select_related(
            'height_cm',
            'years_to_max_height',
            'spread_cm',
            'scientific_classification',
        ),
        slug=slug,
    )
