from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import ForecastPage, HomePage, WarningIndexPage, WarningPage


class Lab05StreamFieldTests(WagtailPageTestCase):
    def setUp(self):
        super().setUp()
        self.root = Page.get_first_root_node()
        self.home = HomePage.objects.first()
        if self.home is None:
            self.home = HomePage(title="Home", slug="home")
            self.root.add_child(instance=self.home)
        self.home.save_revision().publish()

        site = Site.objects.get(is_default_site=True)
        site.root_page = self.home
        site.save()

        self.forecast = ForecastPage(
            title="Public Forecast — Tuesday",
            slug="forecast-tuesday",
            body=[
                ("summary", "<p>Generally fine across Fiji.</p>"),
                (
                    "region_outlook",
                    {"region": "Central Division", "outlook": "Sunny with light winds."},
                ),
                (
                    "region_outlook",
                    {"region": "Northern Division", "outlook": "Isolated showers."},
                ),
                ("hazard", "High UV levels this afternoon"),
            ],
        )
        self.home.add_child(instance=self.forecast)
        self.forecast.save_revision().publish()

    def test_can_create_forecast_under_home(self):
        self.assertCanCreateAt(HomePage, ForecastPage)

    def test_cannot_create_forecast_under_warning_index(self):
        self.assertCanNotCreateAt(WarningIndexPage, ForecastPage)
        self.assertCanNotCreateAt(WarningPage, ForecastPage)

    def test_forecast_page_renders_regions(self):
        response = self.client.get(self.forecast.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Central Division")
        self.assertContains(response, "Sunny with light winds.")
        self.assertContains(response, "Northern Division")
        self.assertContains(response, "High UV levels this afternoon")

    def test_homepage_allows_forecast_subpage_type(self):
        self.assertIn("home.ForecastPage", HomePage.subpage_types)
