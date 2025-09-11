.PHONY: build run stop logs clean clean-cache


# Запуск сервисов в фоновом режиме
run:
	docker compose up -d --build

# Остановка сервисов
stop:
	docker compose stop

# Подключение к логам всех сервисов
logs:
	docker compose logs -f

# Удаление всех контейнеров, сетей и томов
clean:
	docker compose down -v --remove-orphans

# Очистка всех кешей Python
clean-cache:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find .. -type d -name .ruff_cache -exec rm -rf {} +

# Запуск Dockerfile, создание образа
up:
	docker build -t payment_yookassa .

# Запуск образа, создание контейнера
start:
	docker run -d -p 5000:5000 --name payment_yookassa payment_yookassa_build

# Просмотр логов в контейнере
log:
	docker logs payment_yookassa