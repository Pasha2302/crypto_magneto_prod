#!/bin/bash

# Создание директории для логов, если она не существует
mkdir -p Celery_Logs

echo "🚀 Запускаем Celery воркеры и beat ..."

# Воркер для дефолтных задач
nohup celery -A src worker -l info -Q default > Celery_Logs/celery_worker_default.log 2>&1 &

# Воркер для тяжелых задач
# nohup celery -A src worker -l info -Q heavy_tasks --concurrency=2 > Celery_Logs/celery_worker_heavy.log 2>&1 &

# Воркер для быстрых задач
# nohup celery -A src worker -l info -Q fast_tasks --concurrency=4 > Celery_Logs/celery_worker_fast.log 2>&1 &

# Beat для периодических задач
nohup celery -A src beat -l info > Celery_Logs/celery_beat.log 2>&1 &

echo "✅ Все сервисы Celery запущены в фоне. Логи в ./Celery_Logs/"

