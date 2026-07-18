# Marketplace — Образовательная платформа

Онлайн-платформа для образовательных курсов, построенная на Django (backend) и Vue.js (frontend).

## Архитектура проекта

Проект состоит из следующих микросервисов и компонентов:

| Сервис | Описание |
|---------|-------------|
| **nginx** | Обратный прокси для frontend и backend |
| **redis** | Кэширование сессий и фоновых задач |
| **frontend** | Vue.js клиентское приложение |
| **backend** | Django REST API сервер |
| **database** | PostgreSQL база данных |

### Основные модули backend

- **userauth** — аутентификация и управление пользователями
- **courses** — управление курсами
- **author** — управление авторами курсов
- **student** — управление студентами
- **organizations** — управление организациями
- **tariffs** — тарифные планы
- **payments** — обработка платежей (YooKassa)
- **questions** — тесты и вопросы
- **feedback** — отзывы и рейтинги
- **notification** — уведомления (WebSocket)
- **contacts** — контактные формы
- **vuz** — интеграция с вузами

## Технологический стек

### Backend
- Python 3.x
- Django / Django REST Framework
- PostgreSQL 13
- Redis 6
- Uvicorn (ASGI сервер)
- Django Channels (WebSocket)
- YooKassa (платежная система)

### Frontend
- Vue.js 3
- TypeScript
- Vite
- Pinia (state management)
- Axios

### Инфраструктура
- Docker / Docker Compose
- Nginx
- GitLab CI/CD

## Предварительные требования

Перед запуском проекта убедитесь, что у вас установлены:

- [Docker](https://www.docker.com/get-started) (версия 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (версия 1.29+)
- Git
- Make (опционально, для использования команды make)

## Быстрый старт

### 1. Клонирование репозитория

```sh
git clone <url-репозитория>
cd marketplace
```

### 2. Настройка переменных окружения

Скопируйте файлы с примерами конфигурации и заполните их своими значениями:

```sh
# Для backend
cp backend/.env.sample backend/.env.dev

# Для frontend
cp frontend/.env.example frontend/.env.dev
```

Отредактируйте созданные файлы, указав свои значения для переменных окружения.

### 3. Запуск development-окружения

#### Способ 1: Использование скрипта (рекомендуется)

```sh
chmod +x run_dev.sh
./run_dev.sh
```

Скрипт автоматически:
- Копирует env-файлы
- Собирает и запускает контейнеры
- Показывает логи в реальном времени

#### Способ 2: Прямой запуск через Docker Compose

```sh
docker compose -f docker-compose-dev.yml up -d --build
```

### 4. Загрузка начальных данных

После первого запуска и сборки frontend (примерно 5 минут) выполните:

```sh
docker compose -f docker-compose-dev.yml exec backend python manage.py project_start
```

> **Важно:** Первичная загрузка данных может занять до 20 минут.

### 5. Доступ к приложению

Приложение будет доступно по адресу: `http://localhost`

## Переменные окружения

### Backend (`backend/.env.*`)

| Переменная | Описание |
|------------|----------|
| `DEBUG` | Режим отладки Django (True/False) |
| `HOST_URL` | Публичный URL хоста |
| `SECRET_KEY` | Секретный ключ Django (сгенерируйте случайный) |
| `ALLOWED_HOSTS` | Список разрешенных хостов (через запятую) |
| `CSRF_TRUSTED_ORIGINS` | Доверенные источники CSRF (через запятую) |
| `DB_NAME` | Имя базы данных PostgreSQL |
| `DB_USER` | Пользователь PostgreSQL |
| `DB_PASS` | Пароль PostgreSQL |
| `DB_HOST` | Хост PostgreSQL |
| `DB_PORT` | Порт PostgreSQL |
| `YOOKASSA_SHOP_ID` | ID магазина YooKassa (опционально) |
| `YOOKASSA_SECRET_KEY` | Секретный ключ YooKassa (опционально) |
| `EMAIL_HOST` | SMTP сервер для отправки писем |
| `EMAIL_PORT` | Порт SMTP сервера |
| `EMAIL_HOST_USER` | Имя пользователя SMTP |
| `EMAIL_HOST_PASSWORD` | Пароль SMTP |
| `REDIS_HOST` | Хост Redis |
| `REDIS_PORT` | Порт Redis |

### Frontend (`frontend/.env.*`)

| Переменная | Описание |
|------------|----------|
| `VITE_BASE_URL` | Базовый URL backend API |
| `VITE_JIVO_KEY` | Ключ виджета JivoChat (опционально) |
| `VITE_GTM_ID` | Google Tag Manager ID (опционально) |
| `VITE_YANDEX_METRIKA_ID` | Яндекс.Метрика ID (опционально) |

## Сценарии запуска

### Development (разработка)

```sh
docker compose -f docker-compose-dev.yml up -d --build
```

Порт: `http://localhost:80`

### Testing (тестирование)

```sh
docker compose -f docker-compose-test.yml up -d --build
```

### Production (продакшен)

```sh
docker compose -f docker-compose-prod.yml up -d --build
```

## Полезные команды

### Просмотр логов

```sh
# Все логи
docker compose -f docker-compose-dev.yml logs -f

# Логи конкретного сервиса
docker compose -f docker-compose-dev.yml logs -f backend
docker compose -f docker-compose-dev.yml logs -f frontend
docker compose -f docker-compose-dev.yml logs -f database
```

### Остановка контейнеров

```sh
# Остановка development-окружения
docker compose -f docker-compose-dev.yml down

# Остановка с удалением volumes (ВНИМАНИЕ: удалит все данные!)
docker compose -f docker-compose-dev.yml down -v
```

### Выполнение management-команд Django

```sh
# Создание суперпользователя
docker compose -f docker-compose-dev.yml exec backend python manage.py createsuperuser

# Применение миграций
docker compose -f docker-compose-dev.yml exec backend python manage.py migrate

# Создание миграций
docker compose -f docker-compose-dev.yml exec backend python manage.py makemigrations

# Загрузка начальных данных
docker compose -f docker-compose-dev.yml exec backend python manage.py project_start

# Сбор статики
docker compose -f docker-compose-dev.yml exec backend python manage.py collectstatic --noinput

# Запуск тестов
docker compose -f docker-compose-dev.yml exec backend python manage.py test

# Доступ к оболочке Django
docker compose -f docker-compose-dev.yml exec backend python manage.py shell
```

### Работа с базой данных

```sh
# Подключение к PostgreSQL
docker compose -f docker-compose-dev.yml exec database psql -U postgres -d marketplace

# Создание дампа базы данных
docker compose -f docker-compose-dev.yml exec database pg_dump -U postgres marketplace > backup.sql

# Восстановление из дампа
docker compose -f docker-compose-dev.yml exec -T database psql -U postgres -d marketplace < backup.sql
```

### Работа с Redis

```sh
# Подключение к Redis CLI
docker compose -f docker-compose-dev.yml exec redis redis-cli

# Очистка кэша
docker compose -f docker-compose-dev.yml exec redis redis-cli FLUSHALL
```

### Пересборка frontend

```sh
# Пересборка frontend контейнера
docker compose -f docker-compose-dev.yml up -d --build frontend
```

## API документация

После запуска сервера документация API доступна по адресам:

- **Swagger UI**: `http://localhost/swagger/`
- **ReDoc**: `http://localhost/redoc/`

## WebSocket

Система уведомлений использует Django Channels с Redis в качестве брокера сообщений. WebSocket-соединения обрабатываются на уровне ASGI.

## Структура проекта

```
marketplace/
├── backend/                 # Django backend
│   ├── author/              # Авторы курсов
│   ├── contacts/            # Контактные формы
│   ├── core/                # Основные настройки, роутинг, middleware
│   ├── courses/             # Управление курсами
│   ├── feedback/            # Отзывы и рейтинги
│   ├── maintenance/         # Утилиты обслуживания
│   ├── notification/        # Уведомления (WebSocket)
│   ├── organizations/       # Организации
│   ├── payments/            # Платежи (YooKassa)
│   ├── questions/           # Тесты и вопросы
│   ├── student/             # Студенты
│   ├── tariffs/             # Тарифные планы
│   ├── userauth/            # Аутентификация
│   ├── vuz/                 # Интеграция с вузами
│   ├── .env.dev             # Переменные окружения (dev)
│   ├── .env.prod            # Переменные окружения (prod)
│   ├── .env.test            # Переменные окружения (test)
│   ├── .env.sample          # Шаблон переменных окружения
│   ├── manage.py            # Django management script
│   ├── requirements.txt     # Python зависимости
│   └── Dockerfile           # Docker инструкции
├── frontend/                # Vue.js frontend
│   ├── src/                 # Исходный код
│   ├── .env.dev             # Переменные окружения (dev)
│   ├── .env.prod            # Переменные окружения (prod)
│   ├── .env.test            # Переменные окружения (test)
│   ├── .env.example         # Шаблон переменных окружения
│   ├── package.json         # NPM зависимости
│   └── Dockerfile           # Docker инструкции
├── nginx/                   # Nginx конфигурация
│   ├── nginx.conf
│   └── conf.d/
├── docker-compose-dev.yml   # Development окружение
├── docker-compose-test.yml  # Testing окружение
├── docker-compose-prod.yml  # Production окружение
├── run_dev.sh               # Скрипт запуска dev
├── run_test.sh              # Скрипт запуска test
├── run_local.sh             # Скрипт локального запуска
└── Makefile                 # Make команды
```

## CI/CD

Проект включает конфигурацию `.gitlab-ci.yml` для автоматического деплоя:

- Ветка `develop` → dev-окружение
- Ветка `test` → test-окружение
- Ветка `prod` → production-окружение

## Безопасность

- Никогда не коммитьте реальные `.env` файлы с чувствительными данными в version control
- Файлы `.env` уже добавлены в `.gitignore`
- Используйте `.sample` и `.example` файлы как шаблоны
- Генерируйте надежные уникальные `SECRET_KEY` для каждого окружения
- Храните ключи YooKassa, пароли базы данных и email-учетные данные в безопасности
- Используйте разные учетные данные для dev, test и prod окружений

## Устранение неполадок

### Frontend не собирается

```sh
# Очистка кэша npm
docker compose -f docker-compose-dev.yml exec frontend npm cache clean --force

# Пересборка без кэша
docker compose -f docker-compose-dev.yml build --no-cache frontend
```

### База данных не запускается

```sh
# Проверка статуса
docker compose -f docker-compose-dev.yml ps database

# Просмотр логов
docker compose -f docker-compose-dev.yml logs database
```

### Проблемы с миграциями

```sh
# Откат миграций (если нужно)
docker compose -f docker-compose-dev.yml exec backend python manage.py migrate <app_name> zero

# Повторное применение
docker compose -f docker-compose-dev.yml exec backend python manage.py migrate
```

### Очистка всего окружения

```sh
# Остановка и удаление контейнеров, volumes, networks
docker compose -f docker-compose-dev.yml down -v

# Удаление неиспользуемых образов
docker image prune -a
```

## Разработка

### Локальный запуск backend без Docker

```sh
cd backend

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Запуск сервера разработки
python manage.py runserver 0.0.0.0:8000
```

### Локальный запуск frontend без Docker

```sh
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev
```