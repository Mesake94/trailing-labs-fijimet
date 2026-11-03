# Lab 02 — Templates And Rendering

## Goal

Connect page models to HTML templates so the public weather site can display HomePage content.

## Time

45 minutes

## Learning Outcomes

By the end of this lab, participants can:

- Locate Wagtail’s template naming convention
- Render page fields in a template
- Use the `richtext` filter for `RichTextField`
- Replace the default welcome screen with real homepage content

## Background

Wagtail chooses a template from the page model name:

```text
home/templates/home/home_page.html   ← HomePage
```

Inside the template, the current page is `page`.

Rich text must be passed through `|richtext` (load `wagtailcore_tags`).

## Task 1: Find The Template

Open `demo/home/templates/home/home_page.html`.

Answer:

1. What does `{% extends "base.html" %}` do?
2. What is currently included instead of your fields?
3. Why does Wagtail use `home_page.html` for the `HomePage` class?

## Task 2: Render HomePage Fields

Replace the welcome include with content that uses your Lab 01 fields.

Target structure:

```django
{% extends "base.html" %}
{% load wagtailcore_tags %}

{% block body_class %}template-homepage{% endblock %}

{% block content %}
  <section class="hero">
    <h1>{{ page.title }}</h1>
    {% if page.hero_text %}
      <p class="hero-text">{{ page.hero_text }}</p>
    {% endif %}
  </section>

  {% if page.intro %}
    <section class="intro">
      {{ page.intro|richtext }}
    </section>
  {% endif %}
{% endblock %}
```

You may keep simple CSS later; focus on correct field output now.

## Task 3: Edit Content In Admin

1. Open `http://localhost:8000/admin/`
2. Edit the Home page
3. Set `hero_text` to something like: `Fiji Meteorological Service — Public Outlook`
4. Add a short `intro` with a paragraph about public weather information
5. Publish
6. Visit `http://localhost:8000/`

Answer:

1. Did the title come from your custom field or from `Page`?
2. What happens if `hero_text` is left blank and you use `{% if page.hero_text %}`?
3. Why publish after editing?

## Task 4: Design WarningPage Template (Sketch)

You do not need a perfect layout yet. Sketch `warning_page.html` that would show:

- title
- severity
- issued_at
- summary
- body (rich text)

Answer:

1. Which values are plain text vs need `|richtext`?
2. Where should this template file live?

## Questions

1. What variable name does Wagtail provide for the current page in templates?
2. Why is `|richtext` required for `RichTextField`?
3. If the browser shows the old welcome page after your edit, what are two things to check?

## Checkpoint

You are ready for the next lab when you can:

- Point to the template path for a given page model
- Render custom fields and rich text on the homepage
- Confirm changes via the Wagtail admin publish flow
