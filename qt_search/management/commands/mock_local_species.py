import json

from django.core.management.base import BaseCommand
from django.db import transaction

from common.models import SpeciesModel
from common.utils.mock_species import create_db_specie


class Command(BaseCommand):
    def handle(self, *args, **options):  # noqa: C901
        with open('qt_search/management/commands/data/species_local.json', 'r') as f:
            local_species_data = json.load(f)
        for local_species in local_species_data:
            sp = SpeciesModel(**local_species)
            with transaction.atomic():
                create_db_specie(sp)
