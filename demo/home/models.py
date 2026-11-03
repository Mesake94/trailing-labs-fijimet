from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    intro = RichTextField(blank=True)
    hero_text = models.CharField(max_length=200, blank=True)
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_text"),
        FieldPanel("hero_image"),
        FieldPanel("intro"),
    ]

    subpage_types = ["home.WarningIndexPage", "home.ForecastPage"]

    def get_warning_index(self):
        return (
            self.get_children()
            .live()
            .type(WarningIndexPage)
            .specific()
            .first()
        )

    def get_latest_warnings(self, limit=5):
        index = self.get_warning_index()
        if index is None:
            return WarningPage.objects.none()
        return (
            index.get_children()
            .live()
            .type(WarningPage)
            .specific()
            .order_by("-first_published_at")[:limit]
        )

    def get_latest_forecast(self):
        return (
            self.get_children()
            .live()
            .type(ForecastPage)
            .specific()
            .order_by("-first_published_at")
            .first()
        )


class WarningIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.WarningPage"]


class WarningPage(Page):
    SEVERITY_CHOICES = [
        ("advisory", "Advisory"),
        ("moderate", "Moderate"),
        ("severe", "Severe"),
    ]

    summary = models.CharField(max_length=255)
    body = RichTextField()
    issued_at = models.DateTimeField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    station = models.ForeignKey(
        "home.WeatherStation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="warnings",
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("severity"),
        FieldPanel("issued_at"),
        FieldPanel("station"),
        FieldPanel("body"),
    ]

    parent_page_types = ["home.WarningIndexPage"]
    subpage_types = []


class ForecastPage(Page):
    body = StreamField(
        [
            ("summary", blocks.RichTextBlock(required=False)),
            (
                "region_outlook",
                blocks.StructBlock(
                    [
                        ("region", blocks.CharBlock()),
                        ("outlook", blocks.TextBlock()),
                    ]
                ),
            ),
            ("marine", blocks.RichTextBlock(required=False)),
            ("hazard", blocks.CharBlock(required=False)),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


@register_snippet
class WeatherStation(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, help_text="Short station code")
    island = models.CharField(max_length=100, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("code"),
        FieldPanel("island"),
    ]

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ["name"]
