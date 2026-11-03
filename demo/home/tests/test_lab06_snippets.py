from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage, WarningIndexPage, WarningPage, WeatherStation


class Lab06SnippetTests(WagtailPageTestCase):
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

        self.index = WarningIndexPage(title="Warnings", slug="warnings")
        self.home.add_child(instance=self.index)
        self.index.save_revision().publish()

        self.station = WeatherStation.objects.create(
            name="Nadi Airport",
            code="NFFN",
            island="Viti Levu",
        )

        self.warning = WarningPage(
            title="Station Warning",
            slug="station-warning",
            summary="Local advisory",
            body="<p>Details</p>",
            issued_at=timezone.now(),
            severity="advisory",
            station=self.station,
        )
        self.index.add_child(instance=self.warning)
        self.warning.save_revision().publish()

    def test_station_str(self):
        self.assertEqual(str(self.station), "Nadi Airport (NFFN)")

    def test_warning_shows_station(self):
        response = self.client.get(self.warning.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nadi Airport")
        self.assertContains(response, "NFFN")

    def test_deleting_station_nulls_warning_fk(self):
        station_id = self.station.id
        self.station.delete()
        self.warning.refresh_from_db()
        self.assertIsNone(self.warning.station_id)
        self.assertFalse(WeatherStation.objects.filter(id=station_id).exists())

    def test_many_warnings_can_share_station(self):
        other = WarningPage(
            title="Second Warning",
            slug="second-warning",
            summary="Another advisory",
            body="<p>More</p>",
            issued_at=timezone.now(),
            severity="moderate",
            station=self.station,
        )
        self.index.add_child(instance=other)
        other.save_revision().publish()
        self.assertEqual(self.station.warnings.count(), 2)
