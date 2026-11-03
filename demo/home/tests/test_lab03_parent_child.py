from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage, WarningIndexPage, WarningPage


class Lab03ParentChildTests(WagtailPageTestCase):
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

        self.index = WarningIndexPage(
            title="Warnings",
            slug="warnings",
            intro="<p>Current public warnings.</p>",
        )
        self.home.add_child(instance=self.index)
        self.index.save_revision().publish()

    def test_can_create_warning_under_index(self):
        self.assertCanCreateAt(WarningIndexPage, WarningPage)
        self.assertCanCreateAt(HomePage, WarningIndexPage)

    def test_cannot_create_warning_under_home(self):
        self.assertCanNotCreateAt(HomePage, WarningPage)

    def test_warning_cannot_have_children(self):
        self.assertEqual(WarningPage.subpage_types, [])

    def test_index_lists_only_live_children(self):
        live = WarningPage(
            title="Live Warning",
            slug="live-warning",
            summary="Live summary",
            body="<p>Live body</p>",
            issued_at=timezone.now(),
            severity="advisory",
        )
        self.index.add_child(instance=live)
        live.save_revision().publish()

        draft = WarningPage(
            title="Draft Warning",
            slug="draft-warning",
            summary="Draft summary",
            body="<p>Draft body</p>",
            issued_at=timezone.now(),
            severity="moderate",
            live=False,
        )
        self.index.add_child(instance=draft)
        draft.save_revision()

        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Live Warning")
        self.assertNotContains(response, "Draft Warning")
