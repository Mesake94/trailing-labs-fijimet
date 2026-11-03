# Lab 03 — Parent / Child Warning Pages

## Goal

Structure public weather warnings with an index page and child warning pages, and restrict allowed page types.

## Time

60 minutes

## Learning Outcomes

By the end of this lab, participants can:

- Add a listing page type (`WarningIndexPage`)
- Restrict `subpage_types` and `parent_page_types`
- Explain why a weather CMS needs a clear tree
- Create warning pages under the correct parent in admin

## Background

A flat tree (warnings created anywhere) becomes hard for editors.

A common pattern:

```text
Home
└── Warnings (WarningIndexPage)
    ├── Flash Flood Warning — Central
    └── Strong Wind Warning — Maritime
```

Each warning is a `WarningPage`. The index is the only allowed parent.

## Task 1: Add WarningIndexPage

In `demo/home/models.py`, add an index page. Start simple:

```python
class WarningIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["home.WarningPage"]
```

Ensure `WarningPage` (from Lab 01) declares:

```python
parent_page_types = ["home.WarningIndexPage"]
subpage_types = []
```

Also decide what Home may contain, for example:

```python
# on HomePage
subpage_types = ["home.WarningIndexPage"]
```

Adjust if you already need other children later (forecasts in Lab 05).

## Task 2: Migrate And Create Pages

```bash
docker compose run demo python manage.py makemigrations home
docker compose run demo python manage.py migrate
```

In admin:

1. Under Home, add child page → **Warning index** titled `Warnings`
2. Under Warnings, add a **Warning** page
3. Fill severity, issued time, summary, and body
4. Publish both

Answer:

1. Can you create a `WarningPage` directly under Home after your rules? Try it.
2. What error or UI behaviour do you observe?
3. Why is `subpage_types = []` useful on `WarningPage`?

## Task 3: List Children On The Index

Create `demo/home/templates/home/warning_index_page.html` that lists live children:

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block content %}
  <h1>{{ page.title }}</h1>
  {{ page.intro|richtext }}

  <ul class="warning-list">
    {% for warning in page.get_children.live %}
      <li>
        <a href="{% pageurl warning %}">{{ warning.title }}</a>
      </li>
    {% empty %}
      <li>No active warnings.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

Also add `warning_page.html` if you only sketched it in Lab 02 — make it render the warning fields.

Answer:

1. What does `.live` exclude?
2. Why use `{% pageurl warning %}` instead of hard-coded URLs?

## Task 4: Editor Experience

Answer from an editor’s point of view:

1. Where should a duty officer create a new tropical cyclone warning?
2. How does the index help the public browse warnings?
3. What goes wrong if warnings are allowed under any page type?

## Questions

1. What is the difference between `subpage_types` and `parent_page_types`?
2. Why use the string `"home.WarningPage"` instead of the Python class object in those lists?
3. Should `WarningIndexPage` itself be creatable more than once on a small site? Why or why not?

## Checkpoint

You are ready for the next lab when you can:

- Draw the Home → Warnings → Warning tree
- Enforce parent/child rules in models
- List child warnings on an index template
