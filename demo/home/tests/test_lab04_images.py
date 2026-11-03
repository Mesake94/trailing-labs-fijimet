from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage

Image = get_image_model()


class Lab04ImageTests(WagtailPageTestCase):
    def setUp(self):
        super().setUp()
        self.root = Page.get_first_root_node()
        self.home = HomePage.objects.first()
        if self.home is None:
            self.home = HomePage(title="Home", slug="home", hero_text="Outlook")
            self.root.add_child(instance=self.home)
        self.home.hero_text = "Outlook"
        self.home.hero_image = None
        self.home.save()
        self.home.save_revision().publish()

        site = Site.objects.get(is_default_site=True)
        site.root_page = self.home
        site.save()

    def test_homepage_without_image_ok(self):
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Outlook")

    def test_homepage_with_hero_image_renders_img(self):
        image = Image.objects.create(
            title="Satellite",
            file=get_test_image_file(filename="satellite.png"),
        )
        self.home.hero_image = image
        self.home.save()
        self.home.save_revision().publish()

        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<img")
        self.assertContains(response, 'alt="Satellite"')

    def test_hero_image_field_is_optional(self):
        field = HomePage._meta.get_field("hero_image")
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
