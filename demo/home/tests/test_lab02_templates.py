from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage, WarningPage


class Lab02TemplateTests(WagtailPageTestCase):
    def setUp(self):
        super().setUp()
        self.root = Page.get_first_root_node()
        self.home = HomePage.objects.first()
        if self.home is None:
            self.home = HomePage(
                title="Home",
                slug="home",
                hero_text="Fiji Meteorological Service — Public Outlook",
                intro="<p>Public weather information for Fiji.</p>",
            )
            self.root.add_child(instance=self.home)
        else:
            self.home.hero_text = "Fiji Meteorological Service — Public Outlook"
            self.home.intro = "<p>Public weather information for Fiji.</p>"
            self.home.save()
        self.home.save_revision().publish()

        site = Site.objects.get(is_default_site=True)
        site.root_page = self.home
        site.hostname = "localhost"
        site.save()

        self.warning = WarningPage(
            title="Flash Flood Warning",
            slug="flash-flood",
            summary="Heavy rain expected in Central Division",
            body="<p>Move to higher ground if needed.</p>",
            issued_at=timezone.now(),
            severity="severe",
        )
        self.home.add_child(instance=self.warning)
        self.warning.save_revision().publish()

    def test_homepage_renders_hero_and_intro(self):
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fiji Meteorological Service — Public Outlook")
        self.assertContains(response, "Public weather information for Fiji.")
        self.assertNotContains(response, "welcome_page")

    def test_warning_page_renders_fields(self):
        response = self.client.get(self.warning.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flash Flood Warning")
        self.assertContains(response, "Heavy rain expected in Central Division")
        self.assertContains(response, "Severe")
        self.assertContains(response, "Move to higher ground if needed.")
