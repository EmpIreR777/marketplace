# README: Запуск проекта с Docker Compose

## Предварительные требования
Перед запуском убедитесь, что у вас установлены:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Локальный запуск
-  Для запуска compose-проекта указываем другой `compose.yml`
```sh
   docker-compose -f docker-compose.dev.yml up -d
```
### После запуска контейнеров нужно подождать, пока соберется фронтенд (около 5 минут)
- Для загрузки начальных данных нужно прописать команду
```sh
   docker-compose -f docker-compose.dev.yml exec backend python manage.py project_start
```
Приложение станет доступным по пути `http://localhost`


**NOTE** *Сборка может занять около 20 минут (Наполнение базы начальными данными)*

## Настройка переменных окружения
### 1. Создайте файл `.env` в папке `backend`
В корне папки `backend` создайте файл `.env` и добавьте в него следующие переменные:

```env
DEBUG=

# Django
HOST_URL=
SECRET_KEY=
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=

# Database
DB_NAME=
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=

# Юкасса
YOOKASSA_SHOP_ID=
YOOKASSA_SECRET_KEY=

# Email
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

#create db
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Заполните значения согласно вашему окружению.

## Запуск контейнеров
1. Клонируйте репозиторий (если ещё не сделано):
   ```sh
   git clone <repo-url>
   cd <project-folder>
   ```

2. Соберите и запустите контейнеры:
   ```sh
   docker-compose up --build -d
   ```
   Флаг `-d` запускает контейнеры в фоновом режиме.

## Структура контейнеров
- **nginx-proxy** - реверс-прокси для фронтенда и бэкенда.
- **letsencrypt** - SSL-сертификаты через Let's Encrypt.
- **redis** - кэш Redis для хранения сессий и фоновых задач.
- **frontend** - Vue.js клиентское приложение.
- **backend** - Django API-сервер.
- **database** - PostgreSQL база данных.

## Доступы
- **Frontend**: `http://edx.ru`
- **Backend API**: `http://api.edx.ru`

## Остановка контейнеров
Чтобы остановить и удалить контейнеры, выполните:
```sh
docker-compose down
```

## Логи контейнеров
Для просмотра логов конкретного контейнера используйте:
```sh
docker logs -f <container_name>
```
Например, для бэкенда:
```sh
docker logs -f django_backend
```

