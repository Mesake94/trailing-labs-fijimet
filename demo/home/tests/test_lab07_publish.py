from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import ForecastPage, HomePage, WarningIndexPage, WarningPage


class Lab07PublishAndNavTests(WagtailPageTestCase):
    def setUp(self):
        super().setUp()
        self.root = Page.get_first_root_node()
        self.home = HomePage.objects.first()
        if self.home is None:
            self.home = HomePage(
                title="Home",
                slug="home",
                hero_text="Public outlook",
            )
            self.root.add_child(instance=self.home)
        self.home.hero_text = "Public outlook"
        self.home.save()
        self.home.save_revision().publish()

        site = Site.objects.get(is_default_site=True)
        site.root_page = self.home
        site.save()

        self.index = WarningIndexPage(title="Warnings", slug="warnings")
        self.home.add_child(instance=self.index)
        self.index.save_revision().publish()

        self.live_warning = WarningPage(
            title="Live Cyclone Warning",
            slug="live-cyclone",
            summary="Live summary",
            body="<p>Live body</p>",
            issued_at=timezone.now(),
            severity="severe",
        )
        self.index.add_child(instance=self.live_warning)
        self.live_warning.save_revision().publish()

        self.draft_warning = WarningPage(
            title="DRAFT ONLY Training",
            slug="draft-only",
            summary="Draft summary",
            body="<p>Draft body</p>",
            issued_at=timezone.now(),
            severity="moderate",
            live=False,
        )
        self.index.add_child(instance=self.draft_warning)
        self.draft_warning.save_revision()

        self.forecast = ForecastPage(
            title="Public Forecast",
            slug="public-forecast",
            body=[("summary", "<p>Fine weather.</p>")],
        )
        self.home.add_child(instance=self.forecast)
        self.forecast.save_revision().publish()

    def test_home_and_nav_ok(self):
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Warnings")
        self.assertContains(response, "Forecast")
        self.assertContains(response, "Latest warnings")

    def test_draft_excluded_from_index_and_home(self):
        home_response = self.client.get(self.home.url)
        index_response = self.client.get(self.index.url)
        for response in (home_response, index_response):
            self.assertContains(response, "Live Cyclone Warning")
            self.assertNotContains(response, "DRAFT ONLY Training")

    def test_get_latest_warnings_helper(self):
        titles = [w.title for w in self.home.get_latest_warnings()]
        self.assertIn("Live Cyclone Warning", titles)
        self.assertNotIn("DRAFT ONLY Training", titles)

    def test_unpublish_removes_from_public_lists(self):
        self.live_warning.unpublish()
        response = self.client.get(self.home.url)
        self.assertNotContains(response, "Live Cyclone Warning")
