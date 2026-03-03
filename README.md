# Coderr Backend

Coderr is intended to be a small Fiverr clone. It is a backend for a platform for freelance developers, designed as a portfolio project for further training as a backend developer. It builds on an existing frontend and fully supports CRUD operations. The respective frontend repository can be found under the following link:
[Coderr Frontend](https://github.com/Developer-Akademie-Backendkurs/project.Coderr)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [Creating a Superuser](#creating-a-superuser)
- [API Testing with Postman](#api-testing-with-postman)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and profile permissions
- CRUD for offers, orders and profiles.
- Review management and provision of basic information about the platform.
- RESTful API with DRF

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
├── postman/
│   └── postman_collection.json  # Importable Postman collection
├── media/                  # Uploaded files (runtime)
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

To get started with running the application locally,
ensure you have the following prerequisites:

- Python 3.12 or higher
- [Postman](https://www.postman.com/downloads/) (optional, for easy API testing)

## Installation

1. Clone: `git clone https://github.com/Simeon199/Coderr.git && cd Coderr`
2. Virtualenv: `python -m venv env && env\Scripts\activate` (Windows)
3. Install: `pip install -r requirements.txt`
4. Migrate: `python manage.py makemigrations && python manage.py migrate`

## Running the Server

1. Run: `python manage.py runserver`
2. Access the API at `http://127.0.0.1:8000/` in your browser or API client.

This launches Django's built-in development server, allowing you to test the API endpoints locallly. Note that this is for development only.

## Creating a Superuser

To access admin features or perform administrative tasks, create a superuser account:

1. Run `python manage.py createsuperuser`
2. Follow the prompts to enter a username, email, and password.
3. Use the superuser credentials to log in via the Django admin panel at `http://127.0.0.1:8000/admin/` or for API authentication.

This is useful for testing permissions, managing users, and accessing protected endpoints.

## API Testing with Postman

A [Postman Collection](postman/postman_collection.json) is included to help you test the API endpoints.

**How to use:**

1. Install Postman and import the collection from `postman/postman_collection.json`.
2. Set the base URL to `http://127.0.0.1:8000/` and adjust further environment variables if necessary.
3. Use the requests to test and explore API features.

## Contributing

Contributions are always welcome! If you have suggestions for improvements or want to propose changes, feel free to open an issue. Alternatively, consider forking the repository and submitting a pull request.

## License

This project is licensed under the MIT License — © 2026 Simon Kiesner.