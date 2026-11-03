from django.utils import timezone
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage, WarningPage


class Lab01PageModelTests(WagtailPageTestCase):
    def setUp(self):
        super().setUp()
        self.root = Page.get_first_root_node()
        self.home = HomePage(title="Home", slug="lab01-home", hero_text="Public outlook")
        self.root.add_child(instance=self.home)
        self.home.save_revision().publish()

    def test_homepage_has_lab_fields(self):
        field_names = {f.name for f in HomePage._meta.get_fields()}
        self.assertIn("intro", field_names)
        self.assertIn("hero_text", field_names)

    def test_homepage_panels_include_custom_fields(self):
        panel_names = [p.field_name for p in HomePage.content_panels if hasattr(p, "field_name")]
        self.assertIn("hero_text", panel_names)
        self.assertIn("intro", panel_names)

    def test_warning_page_severity_choices(self):
        values = [value for value, _label in WarningPage.SEVERITY_CHOICES]
        self.assertEqual(values, ["advisory", "moderate", "severe"])

    def test_can_create_warning_page_under_home(self):
        warning = WarningPage(
            title="Strong Wind Warning",
            slug="strong-wind",
            summary="Strong winds expected",
            body="<p>Take care outdoors.</p>",
            issued_at=timezone.now(),
            severity="moderate",
        )
        self.home.add_child(instance=warning)
        warning.save_revision().publish()
        self.assertTrue(WarningPage.objects.filter(slug="strong-wind").exists())

    def test_page_provides_title_and_slug(self):
        self.assertEqual(self.home.title, "Home")
        self.assertEqual(self.home.slug, "lab01-home")
        self.assertTrue(hasattr(self.home, "seo_title"))
