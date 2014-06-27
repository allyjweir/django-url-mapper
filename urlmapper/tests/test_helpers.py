from django.test import TestCase

from ..helpers import get_mapped_url, check_mapped_url
from ..models import URLMap
from .. import settings


class TestGetMappedURL(TestCase):

    def setUp(self):
        # App settings are evaluated at module load, so we need to be able to
        # relaod them if we override anything.
        reload(settings)

    def test_key_does_not_exist_error(self):
        with self.assertRaises(KeyError):
            get_mapped_url('invalid')

    def test_key_does_not_exist_without_error(self):
        with self.settings(URLMAPPER_RAISE_EXCEPTION=False):
            reload(settings)
            self.assertEquals(get_mapped_url('invalid'), '')

    def test_url_map_function_no_request(self):
        self.assertEquals(get_mapped_url('test_1'), 'test_1_success')
        self.assertEquals(get_mapped_url('test_2'), 'test_2_success')

    def test_url_map_function_with_request(self):
        self.assertEquals(get_mapped_url('test_1', {}), 'test_1_success')
        self.assertEquals(get_mapped_url('test_2', {}), 'test_2_success')

    def test_url_map_bad_function_error(self):
        with self.settings(URLMAPPER_FUNCTIONS={'test_3': lambda: [][0]}):
            reload(settings)
            with self.assertRaises(IndexError):
                get_mapped_url('test_3')

    def test_url_map_bad_function_without_error(self):
        with self.settings(
            URLMAPPER_FUNCTIONS={'test_3': lambda: [][0]},
            URLMAPPER_RAISE_EXCEPTION=False
        ):
            reload(settings)
            self.assertEquals(get_mapped_url('test_3'), '')

    def test_no_db_mapping_does_not_raise_error(self):
        self.assertEquals(get_mapped_url('test_3'), '')

    def test_db_mapping_returns_value(self):
        URLMap.objects.create(key='test_3', url='test_3_success')
        self.assertEquals(get_mapped_url('test_3'), 'test_3_success')


class TestCheckMappedURL(TestCase):

    def setUp(self):
        URLMap.objects.create(key='test_3', url='test_3_success')
        URLMap.objects.create(key='test_4')

    def test_positives(self):
        self.assertTrue(check_mapped_url('test_1'))
        self.assertTrue(check_mapped_url('test_2'))
        self.assertTrue(check_mapped_url('test_3'))

    def test_negatives(self):
        self.assertFalse(check_mapped_url('test_4'))
        self.assertFalse(check_mapped_url('test_5'))
        self.assertFalse(check_mapped_url('test_6'))
