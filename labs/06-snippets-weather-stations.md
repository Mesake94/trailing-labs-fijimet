# Lab 06 — Snippets: Weather Stations

## Goal

Introduce Wagtail snippets for reusable weather-station records that are not pages in the site tree.

## Time

45 minutes

## Learning Outcomes

By the end of this lab, participants can:

- Register a snippet model
- Explain when to use a snippet instead of a page
- Link a page field to a snippet
- Edit snippets in the Wagtail admin

## Background

A **weather station** (Nadi Airport, Nausori, Rotuma, …) is reference data. It is not a public URL in the page tree by default.

Snippets are ideal for:

- Stations
- Shared contact cards
- Reusable alert labels

Pages can point at snippets with a `ForeignKey` or `ChooserPanel`-friendly relation.

## Task 1: Decide Page vs Snippet

Answer:

1. Why is `WeatherStation` a poor fit as a `Page` subclass for this training app?
2. When *might* a station deserve its own public page later?
3. Should a tropical cyclone warning be a snippet or a page? Why?

## Task 2: Create WeatherStation Snippet

Add a new module or place at the bottom of `demo/home/models.py`:

```python
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


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
```

Migrate, then in admin open **Snippets** → **Weather stations** and add at least three stations.

Answer:

1. Where do snippets appear in the admin compared to pages?
2. Why implement `__str__`?

## Task 3: Link WarningPage To A Station (Optional Field)

Add an optional foreign key on `WarningPage`:

```python
station = models.ForeignKey(
    "home.WeatherStation",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="warnings",
)
```

Include `FieldPanel("station")` in `content_panels`.

Migrate, edit a warning, select a station, publish.

Update `warning_page.html` to show the station name when set.

Answer:

1. What happens to the warning if the snippet is deleted (`SET_NULL`)?
2. Could many warnings share one station? How does the relation model that?

## Task 4: Modelling Choices

Answer:

1. Would severity be better as a snippet, choices on a CharField, or a page? Pick one and justify.
2. Name one FijiMET content type that should remain a page, not a snippet.

## Questions

1. What is the key difference between snippets and pages?
2. Do snippets have slugs and a place in the page tree by default?
3. How do snippets support consistency across many warnings or forecasts?

## Checkpoint

You are ready for the next lab when you can:

- Register and edit a snippet
- Relate a page to a snippet
- Justify page vs snippet for a new content type
