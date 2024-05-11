import json

from django.db import transaction
from django.test import TestCase

from common.models import SpeciesModel
from common.utils.mock_species import create_db_specie
from qt_search.schemas.filter import FiltersSchema

FILTER_VALUES = {
    'search': ('Rosa gallica', {'count': 20520}),  # баг их должно быть 1
    'tag': ('Roses', {'count': 1}),
    'soil_type': ('loam', {'count': 8}),
    'soil_moisture': ('well_drained', {'count': 5}),
    'soil_ph': ('acid', {'count': 8}),
    'position_sunlight': ('partial_shade', {'count': 6}),
    'position_side': ('north_facing', {'count': 4}),
    'edible_part': ('stem', {'count': 1}),
    'fragrance': ('flower', {'count': 2}),
    'harvest': ('autumn', {'count': 1}),
    'planting': ('spring', {'count': 6}),
    'foliage': ('deciduous', {'count': 6}),
    'toxicity': ('toxic_to_dogs', {'count': 3}),
    'habit': ('bushy', {'count': 5}),
    'exposure': ('exposed_or_sheltered', {'count': 3}),
    'duration': ('annual', {'count': 1}),

    'height_cm_from_gte': (1200, {'count': 3}),
    'height_cm_from_lte': (1199, {'count': 5}),
    'height_cm_to_gte': (400, {'count': 3}),
    'height_cm_to_lte': (400, {'count': 3}),

    'years_to_max_height_from_gte': (10, {'count': 6}),
    'years_to_max_height_from_lte': (9, {'count': 2}),
    'years_to_max_height_to_gte': (10, {'count': 6}),
    'years_to_max_height_to_lte': (10, {'count': 2}),

    'spread_cm_from_gte': (228, {'count': 5}),
    'spread_cm_from_lte': (228, {'count': 3}),
    'spread_cm_to_gte': (322, {'count': 1}),
    'spread_cm_to_lte': (322, {'count': 3}),
}

ALL_FILTER_FIELDS = FiltersSchema.model_fields


def mock_data():
    with open('qt_search/management/commands/data/species_local.json', 'r') as f:
        local_species_data = json.load(f)
    for local_species in local_species_data:
        sp = SpeciesModel(**local_species)
        with transaction.atomic():
            create_db_specie(sp)


class ZalupaTestCase(TestCase):
    def setUp(self):
        mock_data()

    def test_ok(self):
        resp = self.client.get('/api/species/')
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data['count'], 10)

    def test_all_filters(self):
        for field in ALL_FILTER_FIELDS:
            self.assertIn(field, FILTER_VALUES)
            filter_data, resp_data = FILTER_VALUES[field]
            resp = self.client.get('/api/species/', {field: filter_data})
            data = resp.json()
            self.assertEqual(data['count'], resp_data['count'])

    def test_wrong_filter(self):
        resp = self.client.get('/api/species/', {'soil_type': 'test'})
        self.assertEqual(resp.status_code, 422)

        for field in ALL_FILTER_FIELDS:
            resp_empty = self.client.get('/api/species/', {'soil_type': field})
            self.assertEqual(resp_empty.status_code, 422)

    def test_negative_filter(self):
        resp = self.client.get('/api/species/', {'height_cm_from_lte': 0})
        self.assertEqual(resp.status_code, 422)

        resp = self.client.get('/api/species/', {'spread_cm_from_lte': -1})
        self.assertEqual(resp.status_code, 422)

    def test_detail_ok(self):
        resp = self.client.get('/api/species/')
        data = resp.json()
        items = data['items']
        slug = items[0].get('slug')
        self.assertIsNotNone(slug)

        resp_detail = self.client.get(f'/api/species/{slug}/')
        self.assertEqual(resp_detail.status_code, 200)

    def test_not_detail(self):
        resp_detail = self.client.get('/api/species/test/')
        self.assertEqual(resp_detail.status_code, 404)

    def test_specific_detail(self):
        resp_detail = self.client.get('/api/species/acer-negundo/')
        self.assertEqual(resp_detail.status_code, 200)

    def test_order(self):
        resp = self.client.get('/api/species/')
        data = resp.json()
        items = data['items']
        slug_first = items[0].get('slug')
        slug_last = items[-1].get('slug')

        resp_first = self.client.get(f'/api/species/{slug_first}/')
        resp_last = self.client.get(f'/api/species/{slug_last}/')
        data_first = resp_first.json()
        data_last = resp_last.json()

        self.assertLess(data_first['rating'], data_last['rating'])

    # Не самый лучший тест, проверять конкретные значения конкретного растения, но это хоть как-то проверяет валидацию.
    def test_detail(self):
        resp_detail = self.client.get('/api/species/acer-negundo/')
        data_detail = resp_detail.json()

        self.assertEqual(data_detail['main_common_name'], 'Box elder')
        self.assertListEqual(
            list(data_detail['images'].keys()),
            ['bark', 'fruit', 'flower', 'habit', 'leaf', 'other', 'root', 'stem', 'seed', 'tuber', 'foliage']
        )
        self.assertListEqual(
            list(data_detail['images']['bark'][0].keys()),
            ['image_url', 'image_copyright']
        )

        self.assertLess(
            data_detail['years_to_max_height']['from_value'],
            data_detail['years_to_max_height']['to_value'],
        )

        self.assertEqual(data_detail['exposure'], {'value': 'sheltered', 'label': 'Sheltered'})
        self.assertEqual(data_detail['duration'], {'value': 'biennial', 'label': 'Biennial'})

        self.assertIn('Trees', data_detail['tags'])
        self.assertIn('Acer negundo', data_detail['synonyms'])
        self.assertIn('Box elder', data_detail['common_names']['eng'])

        self.assertListEqual(
            list(data_detail['pathogens'].keys()),
            ['disease', 'pest']
        )
        self.assertListEqual(
            data_detail['pathogens']['disease'],
            ['Black spot', 'Scars', 'Underwatering', 'Fruit withering']
        )

        self.assertListEqual(
            list(data_detail['growth_tips'].keys()),
            ['propagation', 'suggested_panting_places', 'pruning']
        )
        self.assertEqual(
            data_detail['growth_tips']['propagation'], ['Propagate by seed', 'Grafting']
        )
        self.assertEqual(
            data_detail['growth_tips']['suggested_panting_places'],
            [
                'Cottage and informal garden',
                'Architectural',
                'City and courtyard gardens',
                'Patio and container plants',
                'Low Maintenance'
            ]
        )
        self.assertEqual(data_detail['growth_tips']['pruning'], ['Pruning group 1'])

        self.assertListEqual(
            list(data_detail['parts_color'].keys()),
            ['bark', 'fruit', 'flower', 'habit', 'leaf', 'other', 'root', 'stem', 'seed', 'tuber', 'foliage']
        )
        self.assertListEqual(
            list(data_detail['parts_color']['flower'][0].keys()),
            ['season', 'colors']
        )
        self.assertListEqual(
            data_detail['parts_color']['flower'][0]['colors'],
            ['Green']
        )

        self.assertLess(
            data_detail['regular_events'][0]['frequency']['from_value'],
            data_detail['regular_events'][0]['frequency']['to_value']
        )
        self.assertEqual(
            data_detail['regular_events'][0]['frequency_unit'],
            {'value': 'week', 'label': 'Week'}
        )
        self.assertEqual(data_detail['regular_events'][0]['frequency_count'], 1)

        self.assertEqual(
            list(data_detail['distributions'][0].keys()),
            ['statuses', 'name', 'tdwg_code', 'tdwg_level', 'species_count']
        )
        self.assertEqual(
            data_detail['distributions'][0]['statuses'][0],
            {'value': 'native', 'label': 'Native'}
        )

        self.assertListEqual(
            list(data_detail['sources'][0].keys()),
            ['last_update', 'sid', 'name', 'source_url', 'citation']
        )

        self.assertEqual(data_detail['sources'][0]['last_update'], '2022-12-05T06:04:44.271Z')
        self.assertEqual(data_detail['sources'][0]['sid'], 'wfo-0000514643')
        self.assertEqual(data_detail['sources'][0]['name'], 'WFO')
        self.assertIsNone(data_detail['sources'][0]['source_url'])
        self.assertEqual(data_detail['sources'][0]['citation'], "")

        self.assertIn({'value': 'stem', 'label': 'Stem'}, data_detail['edible_part'])
        self.assertIn({'value': 'clay', 'label': 'Clay'}, data_detail['soil_type'])
        self.assertIn(
            {'value': 'moist_well_drained', 'label': 'Moist but well-drained'},
            data_detail['soil_moisture']
        )
        self.assertIn({'value': 'acid', 'label': 'Acid'}, data_detail['soil_ph'])
        self.assertIn(
            {'value': 'partial_shade', 'label': 'Partial shade'},
            data_detail['position_sunlight']
        )
        self.assertIn(
            {'value': 'east_facing', 'label': 'East-facing'},
            data_detail['position_side']
        )
        self.assertIn({'value': 'bark', 'label': 'Bark'}, data_detail['fragrance'])
        self.assertIn({'value': 'autumn', 'label': 'Autumn'}, data_detail['harvest'])
        self.assertIn({'value': 'spring', 'label': 'Spring'}, data_detail['planting'])
        self.assertIn(
            {'value': 'highly_toxic_to_humans', 'label': 'Highly Toxic to Humans'},
            data_detail['toxicity']
        )
        self.assertIn({'value': 'deciduous', 'label': 'Deciduous'}, data_detail['foliage'])
        self.assertIn(
            {'value': 'columnar_upright', 'label': 'Columnar upright'},
            data_detail['habit']
        )

        self.assertEqual(data_detail['height_cm']['from_value'], 1200)
        self.assertEqual(data_detail['height_cm']['to_value'], None)

        self.assertEqual(data_detail['years_to_max_height']['from_value'], 10)
        self.assertEqual(data_detail['years_to_max_height']['to_value'], 20)

        self.assertEqual(data_detail['spread_cm']['from_value'], 800)
        self.assertEqual(data_detail['spread_cm']['to_value'], None)

        self.assertEqual(data_detail['slug'], 'acer-negundo')
        self.assertEqual(data_detail['rating'], 190)
