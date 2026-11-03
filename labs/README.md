# FijiMET Wagtail Essentials — Labs

Build a basic **public weather CMS** with Wagtail while learning core CMS concepts.

## Prerequisites

1. Complete the Docker setup in the project [README](../README.md).
2. Start the stack: `docker compose up --build`
3. Create a superuser and sign in at `http://localhost:8000/admin/`
4. Skim [docs/Wagtail-Essentials.md](../docs/Wagtail-Essentials.md)

## Lab Path

| Lab | Topic | Time |
| --- | --- | --- |
| [01](01-page-models.md) | Page models (`HomePage`, `WarningPage`) | 60 min |
| [02](02-templates-and-rendering.md) | Templates and rendering | 45 min |
| [03](03-parent-child-warnings.md) | Warning index, parent/child rules | 60 min |
| [04](04-images-and-media.md) | Hero images and the media library | 45 min |
| [05](05-streamfield-forecasts.md) | StreamField forecast pages | 60 min |
| [06](06-snippets-weather-stations.md) | Snippets for weather stations | 45 min |
| [07](07-publish-and-site-tree.md) | Publish workflow and site tree | 45 min |

## How To Work

- Answer questions in your notes or lab worksheet before peeking at docs.
- Edit code under `demo/` (bind-mounted into the container).
- After model changes, always migrate:

```bash
docker compose run demo python manage.py makemigrations
docker compose run demo python manage.py migrate
```

- Restart is usually unnecessary for Python/template edits while `runserver` is up; refresh the browser.

## App Context

You are building content types a meteorological service might use:

- Home landing page
- Public weather warnings
- Regional forecasts
- Reusable weather station records
