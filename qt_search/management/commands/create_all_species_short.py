import json
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from common.models import SpeciesModel
from common.utils.mock_species import create_db_specie

SPECIES_DATA_FOLDER = 'qt_search/management/commands/data/species-data-short'


class Command(BaseCommand):
    def handle(self, *args, **options):  # noqa: C901
        try:
            list_jsons = os.listdir(SPECIES_DATA_FOLDER)
        except FileNotFoundError:
            return
        for json_filename in list_jsons:
            if not json_filename.endswith('.json'):
                continue
            with open(f'{SPECIES_DATA_FOLDER}/{json_filename}', 'r') as json_file:
                json_content = json_file.read()
                data = json.loads(json_content)
                sp = SpeciesModel(**data)
                with transaction.atomic():
                    create_db_specie(sp)
