# Backend — Marketplace API

Django REST API server for the Marketplace education platform.

## Tech Stack

- **Python 3.x** / **Django** / **Django REST Framework**
- **PostgreSQL** — database
- **Redis** — cache & session storage
- **Uvicorn** — ASGI server
- **YooKassa** — payment integration

## Project Structure

```
backend/
├── author/          # Author management
├── contacts/        # Contact forms
├── core/            # Core settings, routing, middleware
├── courses/         # Course management
├── feedback/        # Reviews and feedback
├── maintenance/     # Maintenance utilities
├── notification/    # Notifications (WebSocket)
├── organizations/   # Organization management
├── payments/        # Payment processing (YooKassa)
├── questions/       # Questions & quizzes
├── student/         # Student management
├── tariffs/         # Tariff plans
├── userauth/        # Authentication & user management
├── vuz/             # University integration
├── .env.dev         # Development environment variables
├── .env.prod        # Production environment variables
├── .env.test        # Test environment variables
├── .env.sample      # Environment template
├── manage.py        # Django management script
├── requirements.txt # Python dependencies
└── Dockerfile       # Docker build instructions
```

## Setup

### 1. Environment Configuration

Copy the sample environment file and configure it:

```sh
cp backend/.env.sample backend/.env
```

Edit `backend/.env` with your settings. See `.env.sample` for all available variables.

### 2. Running with Docker

```sh
docker compose -f docker-compose-dev.yml up -d backend database
```

### 3. Running Locally (without Docker)

```sh
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:8000
```

## Management Commands

```sh
# Load initial project data
python manage.py project_start

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic --noinput
```

## API Documentation

API documentation is available via Swagger/OpenAPI at `/swagger/` or `/redoc/` when the server is running.

## WebSocket

The notification system uses Django Channels with Redis as the backing store. WebSocket connections are handled at the ASGI level.