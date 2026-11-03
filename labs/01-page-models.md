# Lab 01 — Page Models

## Goal

Define Wagtail page models — the Python classes that make page types editable and renderable.

## Time

60 minutes

## Learning Outcomes

By the end of this lab, participants can:

- Subclass `Page` to create a page type
- Add custom fields to a page model
- Explain what `Page` already provides
- Describe the migration step required in a real project

## Background

A page type is a Django model that inherits from Wagtail’s `Page`.

`Page` already includes:

- `title`
- `slug`
- SEO / promote fields
- draft and live state
- tree relationships (parent, children)

You add only fields specific to that content type.

In this course we build a **FijiMET public weather CMS**. Lab 01 designs the first page types: home and weather warnings.

Open `demo/home/models.py` — you should see a blank `HomePage` starter.

## Task 1: Read The Base Fields

Answer without looking at code first, then check `docs/Wagtail-Essentials.md`:

1. Why should you not recreate a `title` field on every page model?
2. What does the slug control?
3. Why is inheriting from `Page` required for tree pages?

## Task 2: Design HomePage

Write a `HomePage` model with:

- `intro` — rich text, optional
- `hero_text` — short plain text, optional

Use this structure as your target:

```python
from wagtail.models import Page
from wagtail.fields import RichTextField
from django.db import models
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    intro = RichTextField(blank=True)
    hero_text = models.CharField(max_length=200, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_text"),
        FieldPanel("intro"),
    ]
```

Update `demo/home/models.py` to match.

Answer:

1. Which fields come from `Page` automatically?
2. Why include `Page.content_panels + [...]` instead of replacing panels entirely?

## Task 3: Design WarningPage

Create a `WarningPage` model for public weather warnings with:

| Field | Type | Notes |
| --- | --- | --- |
| `summary` | CharField | Short headline summary |
| `body` | RichTextField | Full warning text |
| `issued_at` | DateTimeField | When the warning was issued |
| `severity` | CharField | e.g. Advisory / Moderate / Severe |

Write the full model class in `demo/home/models.py`, including `content_panels`.

Optional: use `choices` for `severity`.

Example severity choices:

```python
SEVERITY_CHOICES = [
    ("advisory", "Advisory"),
    ("moderate", "Moderate"),
    ("severe", "Severe"),
]
```

## Task 4: Parent / Child Page Types

In a real Wagtail project you often restrict which page types can be created under which parents.

Answer:

1. Should `WarningPage` be creatable directly under Home? Why or why not?
2. What page type should be the parent of warning pages?
3. Why do developers limit allowed subpage types?

(You will implement index + rules in Lab 03. For now, design the answer.)

## Task 5: Migrations Mindset

After saving your models, run:

```bash
docker compose run demo python manage.py makemigrations home
docker compose run demo python manage.py migrate
```

Answer:

1. What do migrations create for a new page model?
2. Why must page models be included in an installed Django app?
3. What breaks if you add fields but forget migrations?

## Questions

1. What is the difference between a page model and a page instance?
2. How many `HomePage` instances should a simple site usually have?
3. When would a forecast be a page model instead of only a Django model?

## Checkpoint

You are ready for the next lab when you can:

- Write a basic `Page` subclass
- List fields inherited from `Page`
- Explain that migrations are required before the admin can use the new type
