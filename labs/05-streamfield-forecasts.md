# Lab 05 — StreamField Forecasts

## Goal

Build a flexible `ForecastPage` using StreamField so editors can compose regional outlook sections without new migrations for every layout tweak.

## Time

60 minutes

## Learning Outcomes

By the end of this lab, participants can:

- Define a `StreamField` with several block types
- Explain when StreamField beats a fixed set of model fields
- Render StreamField content in a template
- Place forecast pages correctly in the site tree

## Background

A daily forecast page might need:

- A lead summary
- One or more regional outlooks
- Optional marine notes
- Optional hazard callouts

Fixed fields (`region_1_text`, `region_2_text`, …) do not scale. StreamField lets editors add blocks in order.

## Task 1: Design Blocks On Paper

List 3–5 block types useful for a Fiji public forecast. Examples:

| Block name | Purpose |
| --- | --- |
| `summary` | Lead paragraph for the day |
| `region_outlook` | Region name + outlook text |
| `marine` | Marine forecast note |
| `hazard` | Short hazard callout |

Answer:

1. Which of these would be awkward as a single mandatory model field?
2. Why might `region_outlook` be a `StructBlock` instead of two independent blocks?

## Task 2: Implement ForecastPage

Add to `demo/home/models.py` (adjust imports as needed):

```python
from wagtail import blocks
from wagtail.fields import StreamField


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
```

Update `HomePage.subpage_types` so Home can contain both the warning index and forecasts, for example:

```python
subpage_types = ["home.WarningIndexPage", "home.ForecastPage"]
```

Migrate after saving.

## Task 3: Template For StreamField

Create `demo/home/templates/home/forecast_page.html`:

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block content %}
  <h1>{{ page.title }}</h1>

  {% for block in page.body %}
    <section class="block-{{ block.block_type }}">
      {% if block.block_type == "summary" %}
        {{ block.value|richtext }}
      {% elif block.block_type == "region_outlook" %}
        <h2>{{ block.value.region }}</h2>
        <p>{{ block.value.outlook }}</p>
      {% elif block.block_type == "marine" %}
        {{ block.value|richtext }}
      {% elif block.block_type == "hazard" %}
        <p class="hazard"><strong>{{ block.value }}</strong></p>
      {% endif %}
    </section>
  {% endfor %}
{% endblock %}
```

## Task 4: Create A Sample Forecast

In admin, under Home, create **Forecast** titled e.g. `Public Forecast — Tuesday`.

Add:

- one summary block
- at least two region outlook blocks (e.g. Central Division, Northern Division)
- one hazard or marine block

Publish and view the page.

Answer:

1. How did reordering blocks in the admin change the public page?
2. Did you need a migration to add a third region outlook? Why or why not?
3. When would you still use a normal `CharField` instead of StreamField?

## Questions

1. What problem does StreamField solve for forecast editors?
2. What is a `StructBlock`?
3. Why set `use_json_field=True` on modern Wagtail projects?

## Checkpoint

You are ready for the next lab when you can:

- Define a StreamField with mixed blocks
- Render each block type in a template
- Explain why forecasts fit StreamField well
