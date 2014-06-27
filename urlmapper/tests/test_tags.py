from django.template import Template, Context
from django.test import TestCase

from ..import settings
from ..models import URLMap


class TestTags(TestCase):

    def setUp(self):
        self.context = Context({'request': None})
        self.template = Template("""
        {% load urlmapper_tags %}
        test_1_is_mapped:({{ 'test_1'|is_mapped_url }})
        test_2_is_mapped:({{ 'test_2'|is_mapped_url }})
        test_3_is_mapped:({{ 'test_3'|is_mapped_url }})
        test_4_is_mapped:({{ 'test_4'|is_mapped_url }})
        test_5_is_mapped:({{ 'test_5'|is_mapped_url }})
        test_6_is_mapped:({{ 'test_6'|is_mapped_url }})

        test_1_url:({% mapped_url 'test_1' %})
        test_2_url:({% mapped_url 'test_2' %})
        test_3_url:({% mapped_url 'test_3' %})
        test_4_url:({% mapped_url 'test_4' %})
        test_5_url:({% mapped_url 'test_5' %})
        test_6_url:({% mapped_url 'test_6' %})
        """)
        URLMap.objects.create(key='test_3', url='test_3_success')
        URLMap.objects.create(key='test_4')

    def test_output(self):
        with self.settings(URLMAPPER_RAISE_EXCEPTION=False):
            reload(settings)
            output = self.template.render(self.context)
            self.assertIn("test_1_is_mapped:(True)", output)
            self.assertIn("test_2_is_mapped:(True)", output)
            self.assertIn("test_3_is_mapped:(True)", output)
            self.assertIn("test_4_is_mapped:(False)", output)
            self.assertIn("test_5_is_mapped:(False)", output)
            self.assertIn("test_6_is_mapped:(False)", output)
            self.assertIn("test_1_url:(test_1_success)", output)
            self.assertIn("test_2_url:(test_2_success)", output)
            self.assertIn("test_3_url:(test_3_success)", output)
            self.assertIn("test_4_url:()", output)
            self.assertIn("test_5_url:()", output)
            self.assertIn("test_6_url:()", output)
