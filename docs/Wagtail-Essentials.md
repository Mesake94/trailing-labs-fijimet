# Wagtail Essentials Reference

Supporting notes for the FijiMET Wagtail weather-app labs.

## What Wagtail Adds To Django

Wagtail is a CMS built on Django. You still use Django apps, models, migrations, and templates. Wagtail adds:

- A page tree (hierarchical content)
- Draft / live publishing
- An editor-friendly admin at `/admin/`
- Fields and panels designed for content teams
- Images, documents, snippets, and StreamField

## The Page Model

Every tree page type subclasses `wagtail.models.Page`.

`Page` already provides:

| Field / concept | Role |
| --- | --- |
| `title` | Primary display title |
| `slug` | URL segment for this page |
| SEO / promote fields | Search listing title, description, etc. |
| Draft and live state | Editors can save drafts and publish |
| Tree relationships | Parent, children, siblings |

Do **not** redefine `title` or `slug` on your subclasses. Add only fields specific to that content type.

### Example

```python
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    intro = RichTextField(blank=True)
    hero_text = models.CharField(max_length=200, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_text"),
        FieldPanel("intro"),
    ]
```

`content_panels` controls what editors see in the Content tab. Always extend `Page.content_panels` unless you have a strong reason not to — otherwise you lose the title field in the editor.

## Page Model vs Page Instance

- **Page model** = the Python class (`HomePage`, `WarningPage`) — a *type*
- **Page instance** = one row in the tree (e.g. the site homepage, or “Tropical Cyclone Alert — 3 Nov”)

A simple site usually has **one** `HomePage` instance at the root of the public tree.

## Parent And Child Types

Restrict what can be created under a parent with:

```python
# On the parent
subpage_types = ["home.WarningPage"]

# On the child
parent_page_types = ["home.WarningIndexPage"]
```

Use app labels (`home.WarningPage`) that match your Django app and model names.

Limiting types keeps the tree tidy for editors and prevents invalid structures (e.g. a warning nested under another warning forever).

## Templates

Wagtail looks for templates by convention:

```text
<app>/templates/<app>/<model_name_underscored>.html
```

Example: `HomePage` in app `home` → `home/templates/home/home_page.html`

In templates, the page instance is available as `page` (and often `self`).

```django
{% extends "base.html" %}

{% block content %}
  <h1>{{ page.title }}</h1>
  <p class="hero">{{ page.hero_text }}</p>
  {{ page.intro|richtext }}
{% endblock %}
```

Use the `richtext` filter for `RichTextField` output. Load it with `{% load wagtailcore_tags %}`.

## Images

Use `ForeignKey` to Wagtail’s image model:

```python
from django.db import models
from wagtail.images import get_image_model_string
from wagtail.admin.panels import FieldPanel

hero_image = models.ForeignKey(
    get_image_model_string(),
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="+",
)
```

In templates:

```django
{% load wagtailimages_tags %}
{% image page.hero_image fill-1200x400 as hero %}
<img src="{{ hero.url }}" alt="{{ page.hero_image.title }}">
```

## StreamField

StreamField stores a sequence of typed blocks — useful when forecast sections vary:

```python
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel

body = StreamField([
    ("heading", blocks.CharBlock()),
    ("paragraph", blocks.RichTextBlock()),
    ("outlook", blocks.StructBlock([
        ("region", blocks.CharBlock()),
        ("summary", blocks.TextBlock()),
    ])),
], use_json_field=True, blank=True)

content_panels = Page.content_panels + [
    FieldPanel("body"),
]
```

## Snippets

Snippets are reusable non-page models (stations, severity labels, contacts) edited outside the page tree:

```python
from wagtail.snippets.models import register_snippet
from django.db import models

@register_snippet
class WeatherStation(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name
```

Pages can `ForeignKey` to snippets when needed.

## Migrations

After changing models:

```bash
docker compose run demo python manage.py makemigrations
docker compose run demo python manage.py migrate
```

Migrations create/alter database tables for your fields. Page models must live in an app listed in `INSTALLED_APPS`. Without migrations, the admin and database schema disagree — saves fail or fields are missing.

## FijiMET Weather App Story

Across these labs you design a small public weather CMS:

| Page / model | Purpose |
| --- | --- |
| `HomePage` | Landing page with intro and hero |
| `WarningIndexPage` | Lists public warnings |
| `WarningPage` | One weather warning |
| `ForecastPage` | Flexible forecast with StreamField |
| `WeatherStation` | Snippet for station metadata |

This mirrors how a meteorological service might publish warnings and outlooks for the public.
