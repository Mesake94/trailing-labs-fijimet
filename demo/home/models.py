from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page


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

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("severity"),
        FieldPanel("issued_at"),
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
