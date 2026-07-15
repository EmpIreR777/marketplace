# Marketplace

An online education marketplace platform built with Django (backend) and Vue.js (frontend).

## Architecture

The project consists of the following services:

| Service | Description |
|---------|-------------|
| **nginx-proxy** | Reverse proxy for frontend and backend |
| **letsencrypt** | SSL certificate management via Let's Encrypt |
| **redis** | Cache for sessions and background tasks |
| **frontend** | Vue.js client application |
| **backend** | Django REST API server |
| **database** | PostgreSQL database |

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start (Development)

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd marketplace
   ```

2. Set up environment variables:
   ```sh
   cp backend/.env.sample backend/.env.dev
   cp frontend/.env.example frontend/.env.dev
   ```
   Edit the files and fill in your values.

3. Start the development environment:
   ```sh
   docker compose -f docker-compose-dev.yml up -d
   ```

4. Wait for the frontend to build (approx. 5 minutes), then load initial data:
   ```sh
   docker compose -f docker-compose-dev.yml exec backend python manage.py project_start
   ```

5. The application will be available at `http://localhost`

> **Note:** Initial data loading may take up to 20 minutes.

## Environment Files

### Backend (`backend/.env.*`)

| Variable | Description |
|----------|-------------|
| `DEBUG` | Django debug mode (True/False) |
| `HOST_URL` | Public host URL |
| `SECRET_KEY` | Django secret key (generate a random one) |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASS` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `YOOKASSA_SHOP_ID` | YooKassa shop ID (optional) |
| `YOOKASSA_SECRET_KEY` | YooKassa secret key (optional) |
| `EMAIL_HOST` | SMTP server host |
| `EMAIL_PORT` | SMTP server port |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `REDIS_HOST` | Redis host |

### Frontend (`frontend/.env.*`)

| Variable | Description |
|----------|-------------|
| `VITE_BASE_URL` | Backend API base URL |
| `VITE_JIVO_KEY` | JivoChat widget key (optional) |
| `VITE_GTM_ID` | Google Tag Manager ID (optional) |
| `VITE_YANDEX_METRIKA_ID` | Yandex Metrika ID (optional) |

## Deployment

### Environments

The project supports three environments:

- **dev** — development (`docker-compose-dev.yml`)
- **test** — testing (`docker-compose-test.yml`)
- **prod** — production (`docker-compose-prod.yml`)

Each environment uses its own `.env` file:
- `backend/.env.dev` / `frontend/.env.dev`
- `backend/.env.test` / `frontend/.env.test`
- `backend/.env.prod` / `frontend/.env.prod`

### Production Deployment

1. Copy and configure environment files:
   ```sh
   cp backend/.env.sample backend/.env.prod
   cp frontend/.env.example frontend/.env.prod
   ```

2. Build and start containers:
   ```sh
   docker compose -f docker-compose-prod.yml up -d --build
   ```

### CI/CD

The project includes a `.gitlab-ci.yml` configuration for automated deployment to GitLab CI/CD pipelines. It deploys to the appropriate environment based on the branch:
- `develop` branch → dev environment
- `test` branch → test environment
- `prod` branch → production environment

## Useful Commands

### View logs
```sh
docker compose logs -f <service-name>
```

### Stop all containers
```sh
docker compose -f docker-compose-dev.yml down
```

### Run management commands
```sh
docker compose -f docker-compose-dev.yml exec backend python manage.py <command>
```

## Security Notes

- Never commit real `.env` files with sensitive data to version control
- The `.gitignore` already excludes `.env` files
- Use the `.sample` and `.example` files as templates
- Generate strong, unique `SECRET_KEY` for each environment
- Keep YooKassa keys, database passwords, and email credentials secure