# Coderr Backend

Coderr is intended to be a small Fiverr clone. It is a backend for a platform for freelance developers, designed as a portfolio project for further training as a backend developer. It builds on an existing frontend and fully supports CRUD operations. The respective frontend repository can be found under the following link:
[Coderr Frontend](https://github.com/Developer-Akademie-Backendkurs/project.Coderr)

**Live API:** https://coderr-sk-2026-633433832477.europe-west1.run.app

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Server](#running-the-server)
- [Creating a Superuser](#creating-a-superuser)
- [API Testing with Postman](#api-testing-with-postman)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and profile permissions
- CRUD for offers, orders and profiles
- Review management and provision of basic information about the platform
- RESTful API with DRF
- File uploads via Cloudinary (production) or local filesystem (development)

## Project Structure

The project follows a modular Django architecture. Each feature domain is encapsulated in its own Django app, all sharing a consistent internal layout.

```
Coderr/
├── core/                   # Django project configuration
│   ├── settings.py         # Global settings
│   ├── urls.py             # Root URL dispatcher
│   ├── asgi.py
│   └── wsgi.py
│
├── auth_app/               # Registration and login
├── profile_app/            # User profiles (business & customer)
├── offers_app/             # Offers and offer details
├── orders_app/             # Order management
├── reviews_app/            # Review system
├── base_info_app/          # Platform statistics and base info
├── upload_app/             # Profile image upload
│
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD: tests + Cloud Run deployment
├── media/                  # Uploaded files (local development only)
├── Dockerfile
├── .dockerignore
├── manage.py
├── requirements.txt
└── pytest.ini
```

Each app (except `core`) follows the same internal structure:

```
<app>/
├── models.py           # Data models
├── admin.py            # Django admin registration
├── views.py            # Entry point (delegates to api/)
├── migrations/         # Database migrations
├── tests/              # Unit and integration tests
└── api/
    ├── serializers.py  # DRF serializers
    ├── views.py        # API view logic
    ├── urls.py         # App-level URL patterns
    └── permissions.py  # Custom permissions (where applicable)
```

## Prerequisites

- Python 3.12 or higher

## Installation

1. Clone: `git clone https://github.com/Simeon199/Coderr.git && cd Coderr`
2. Virtualenv: `python -m venv env && env\Scripts\activate` (Windows)
3. Install: `pip install -r requirements.txt`
4. Configure environment variables (see [Environment Variables](#environment-variables))
5. Migrate: `python manage.py migrate`

## Environment Variables

The project reads all configuration from environment variables. For local development, set them in your shell or create a `.env` file and load it with a tool like [python-dotenv](https://pypi.org/project/python-dotenv/).

### Required

| Variable | Description | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `127.0.0.1,localhost` |

### Optional — required only for production parity

| Variable | Description | Fallback (local) |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string (e.g. Neon) | SQLite (`db.sqlite3`) |
| `CLOUDINARY_URL` | Cloudinary connection string | Local filesystem (`media/`) |
| `FRONTEND_URL` | Public frontend origin for CORS | `http://127.0.0.1:5500` and `http://127.0.0.1:8000` are always allowed |

**Without `DATABASE_URL`**, the project uses SQLite automatically — no setup needed for local testing.

**Without `CLOUDINARY_URL`**, uploaded files are stored in the local `media/` directory and served via Django's dev server.

### Minimal `.env` for local development

```
DJANGO_SECRET_KEY=any-local-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

To load a `.env` file automatically, install python-dotenv and add the following to `manage.py` before `execute_from_command_line`:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Running the Server

1. Run: `python manage.py runserver`
2. Access the API at `http://127.0.0.1:8000/`

This launches Django's built-in development server, allowing you to test the API endpoints locally. Note that this is for development only.

## Creating a Superuser

To access admin features or perform administrative tasks, create a superuser account:

1. Run `python manage.py createsuperuser`
2. Follow the prompts to enter a username, email, and password.
3. Use the superuser credentials to log in via the Django admin panel at `http://127.0.0.1:8000/admin/`.

## Deployment

The project is deployed on **Google Cloud Run** via a Docker container. Deployment is fully automated through GitHub Actions.

**Stack:**
- Runtime: Google Cloud Run (europe-west1)
- Database: PostgreSQL via [Neon](https://neon.tech) (free tier)
- File storage: [Cloudinary](https://cloudinary.com) (free tier)
- CI/CD: GitHub Actions (`.github/workflows/deploy.yml`)

**Pipeline:** Every push to `main` triggers the workflow — tests run first, and on success the container is built and deployed to Cloud Run automatically.

**Required GitHub Secrets** for the pipeline to work:

| Secret | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Production secret key |
| `GCP_SA_KEY` | Google Cloud service account JSON key |
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `CLOUDINARY_URL` | Cloudinary connection string |

## Contributing

Contributions are always welcome! If you have suggestions for improvements or want to propose changes, feel free to open an issue. Alternatively, consider forking the repository and submitting a pull request.

## License

This project is licensed under the MIT License — © 2026 Simon Kiesner.
