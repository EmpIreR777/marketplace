#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Настройка окружения для test
export ENVIRONMENT=test
export PYTHONDONTWRITEBYTECODE=1

# Функция для копирования env-файлов с принудительной перезаписью
copy_env_file_force() {
    local template_file=$1
    local target_file=$2
    local service_name=$3

    echo -e "\n=== Обработка ${service_name} ==="

    # Проверка существования исходного файла
    if [[ ! -e "${template_file}" ]]; then
        echo "  ⚠️ Ошибка: исходный файл ${template_file} не найден"
        echo "  Убедитесь, что файл существует по указанному пути"
        return 1
    fi

    # Принудительное копирование с перезаписью
    cp -f "${template_file}" "${target_file}"
    echo "  ✅ Успешно: файл ${target_file} перезаписан"
}

# Обработка backend
copy_env_file_force "backend/.env.test" "backend/.env" "Backend"

# Обработка frontend
copy_env_file_force "frontend/.env.test" "frontend/.env" "Frontend"

echo -e "\nГотово! Все .env файлы были обновлены."

# Запуск контейнеров
docker compose -f docker-compose-test.yml up -d --build

# Включение логов
docker compose -f docker-compose-test.yml logs -f No newline at end of file
