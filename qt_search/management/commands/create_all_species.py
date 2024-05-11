import json
import os
import zipfile

from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from common.models import SpeciesModel
from common.utils.mock_species import create_db_specie

SPECIES_DATA_FOLDER = 'qt_search/management/commands/data/species-data'


class Command(BaseCommand):
    def handle(self, *args, **options):  # noqa: C901
        try:
            list_zips = os.listdir(SPECIES_DATA_FOLDER)
        except FileNotFoundError:
            return
        for zip_filename in list_zips:
            if not zip_filename.endswith('.zip'):
                continue
            with zipfile.ZipFile(f'{SPECIES_DATA_FOLDER}/{zip_filename}', 'r') as zip_file:
                for json_filename in tqdm(zip_file.namelist()):
                    if not json_filename.endswith('.json'):
                        continue
                    with zip_file.open(json_filename) as json_file:
                        json_content = json_file.read()
                        data = json.loads(json_content)
                        sp = SpeciesModel(**data)
                        with transaction.atomic():
                            create_db_specie(sp)
