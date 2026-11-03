# FijiMET Wagtail Docker Training

A Wagtail project configured to run with Docker Compose, plus labs that build a **basic public weather CMS**.

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repository.
2. Create `secrets/app.env` with at least:

```env
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=Pacific/Fiji
```

3. Build and start the environment:

```bash
docker compose up --build
```

## Accessing the app

Open a browser and visit:

```text
http://localhost:8000
```

Wagtail admin:

```text
http://localhost:8000/admin/
```

Create an admin user (in another terminal):

```bash
docker compose run demo python manage.py createsuperuser
```

## Labs

Work through the weather-app labs in order:

- [labs/README.md](labs/README.md) — lab path and how to work
- [docs/Wagtail-Essentials.md](docs/Wagtail-Essentials.md) — reference notes

| Lab | Topic |
| --- | --- |
| [01](labs/01-page-models.md) | Page models |
| [02](labs/02-templates-and-rendering.md) | Templates |
| [03](labs/03-parent-child-warnings.md) | Warning index / parent-child |
| [04](labs/04-images-and-media.md) | Images |
| [05](labs/05-streamfield-forecasts.md) | StreamField forecasts |
| [06](labs/06-snippets-weather-stations.md) | Snippets |
| [07](labs/07-publish-and-site-tree.md) | Publish and site tree |

`demo/home/models.py` starts with a blank `HomePage` — Lab 01 builds from there.

## Useful commands

- Start services:

```bash
docker compose up
```

- Stop services:

```bash
docker compose down
```

- Run Django / Wagtail management commands:

```bash
docker compose run demo python manage.py <command>
```

- Create migrations:

```bash
docker compose run demo python manage.py makemigrations
```

- Apply migrations:

```bash
docker compose run demo python manage.py migrate
```

- Collect static files:

```bash
docker compose run demo python manage.py collectstatic --noinput
```

## Notes

- The Wagtail app runs in the Compose service named `demo`.
- The app uses SQLite (`demo/db.sqlite3`); there is no separate database service.
- Source is bind-mounted from `./demo` to `/app` for local development.
- Adjust volumes and ports as needed for local development.
# trailing-labs-fijimet
