# FijiMET Wagtail Docker Training

A Wagtail project configured to run with Docker Compose for a **basic public weather CMS**.

`main` contains the completed app. History is organized as lab commits (`lab 01` … `lab 07`) so instructors can check out earlier checkpoints.

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

Local lab sheets and reference notes live under `labs/` and `docs/` (gitignored). Work through them in order against this codebase; use git history to reset to a prior lab commit if needed.

| Lab | Topic | Commit message prefix |
| --- | --- | --- |
| 01 | Page models | `lab 01:` |
| 02 | Templates | `lab 02:` |
| 03 | Warning index / parent-child | `lab 03:` |
| 04 | Images | `lab 04:` |
| 05 | StreamField forecasts | `lab 05:` |
| 06 | Snippets | `lab 06:` |
| 07 | Publish and site tree | `lab 07:` |

## Tests

```bash
docker compose run --rm demo python manage.py test home
```

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
- Uploaded media is stored under `demo/media/` (local only).
- Adjust volumes and ports as needed for local development.
