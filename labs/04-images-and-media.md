# Lab 04 — Images And Media

## Goal

Add a hero image to the weather homepage and learn how Wagtail’s image library works for public pages.

## Time

45 minutes

## Learning Outcomes

By the end of this lab, participants can:

- Attach a Wagtail image field to a page model
- Upload and select images in the admin
- Rendition images in templates with `{% image %}`
- Explain why CMS image fields differ from hard-coded static files

## Background

Meteorological sites often show a banner map, satellite still, or campaign image on the home page.

Wagtail stores images in its media library. Pages hold a `ForeignKey` to an image; templates request a **rendition** (resized crop) for the layout.

See `docs/Wagtail-Essentials.md` → Images.

## Task 1: Add hero_image To HomePage

Update `HomePage` in `demo/home/models.py`:

```python
from wagtail.images import get_image_model_string

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
```

Migrate:

```bash
docker compose run demo python manage.py makemigrations home
docker compose run demo python manage.py migrate
```

Answer:

1. Why use `null=True, blank=True` for the image?
2. What does `on_delete=models.SET_NULL` protect you from?
3. Why is `related_name="+"` commonly used here?

## Task 2: Upload And Select

1. In admin, open **Images** and upload a weather-related image (any JPG/PNG is fine for training)
2. Edit Home → set **Hero image**
3. Publish

Answer:

1. Where does the binary file live in the project after upload?
2. Why is uploading through Wagtail better than dropping files only into `static/` for editor-managed banners?

## Task 3: Render A Rendition

Update `home_page.html`:

```django
{% load wagtailcore_tags wagtailimages_tags %}

{% block content %}
  <section class="hero">
    <h1>{{ page.title }}</h1>
    {% if page.hero_text %}
      <p class="hero-text">{{ page.hero_text }}</p>
    {% endif %}
    {% if page.hero_image %}
      {% image page.hero_image fill-1200x400 as hero %}
      <img src="{{ hero.url }}" alt="{{ page.hero_image.title }}">
    {% endif %}
  </section>
  {# intro as before #}
{% endblock %}
```

Answer:

1. What does `fill-1200x400` mean?
2. Name one other rendition filter you might use for a thumbnail list of warnings
3. What should `alt` text describe for accessibility on a public MET site?

## Task 4: Optional — Warning Map Image

Design (do not require full implementation unless time allows) an optional `map_image` on `WarningPage`.

Answer:

1. When is a per-warning map useful?
2. When would a shared static map in `static/` be enough instead?

## Questions

1. What is the difference between an original uploaded image and a rendition?
2. Why keep `hero_image` optional on HomePage?
3. How do images relate to drafts vs published pages when you change the selected image?

## Checkpoint

You are ready for the next lab when you can:

- Add an image `ForeignKey` to a page
- Upload and assign an image in admin
- Output a sized rendition in a template
