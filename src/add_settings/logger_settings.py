from pathlib import Path
import logfire

# ==============================================  Настройки Logfire: ================================================ #

def get_logfire_settings(os, base_dir: Path):
    # Создаем папку logs если ее нет
    logs_dir = base_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)  # exist_ok=True - не создает если уже есть

    logging = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfire': {
                'class': 'logfire.LogfireLoggingHandler',
            },
        },
        'root': {
            'handlers': ['logfire'],
        },
    }

    logfire_configure = logfire.configure(
        service_name="crypto-magneto",
        environment="development",
        token='pylf_v1_us_lbkT4Ny2cRx4ZGzGYpnpzsY6s3FVTvbFwGhJ1Rshs2tC',
        # min_level='debug'  # опционально
    )
    logfire.instrument_django(
        # Игнорировать логирование статики (и других запросов...)
        # excluded_urls=r"^http://127.0.0.1:8000/media/.*",
        excluded_urls=r".*/media/.*|.*/static/.*|.*/favicon\.ico$",
    )


    return logging, logfire_configure


# ======================================================================================================

def get_logger_settings(os, base_dir: Path):
    # Создаем папку logs если ее нет
    logs_dir = base_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)  # exist_ok=True - не создает если уже есть

    data_loggers = {
        'version': 1,
        'disable_existing_loggers': False,  # Не отключаем существующие логгеры

        # Форматы логов - как будет выглядеть каждая строка в лог-файле
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },

        # Обработчики - куда и как писать логи (файлы, консоль и т.д.)
        'handlers': {
            # Общий лог для всего приложения
            'general_file': {
                'level': 'INFO',  # Уровень логирования: DEBUG, INFO, WARNING, ERROR
                'class': 'logging.FileHandler',  # Пишем в файл
                'filename': os.path.join(logs_dir, 'general.log'),
                'formatter': 'verbose'  # Используем подробный формат
            },

            # Лог для админки
            'admin_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, 'admin.log'),
                'formatter': 'verbose'
            },

            # Лог сигналов:
            'signals_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, 'signals.log'),
                'formatter': 'verbose'
            },

            # Лог файл для Задачь Celery
            'tasks_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, 'tasks.log'),
                'formatter': 'verbose'
            },

            'views_file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, 'views.log'),
                'formatter': 'verbose'
            },

            'db_models': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, 'db_models.log'),
                'formatter': 'verbose'
            },

        },

        # Логгеры - определяем какие модули куда пишут логи
        # !! app.db_models - Это имя логгера, которое мы придумываем сами для иерархической группировки.
        'loggers': {
            # Логгер для Django фреймворка
            'django': {
                'handlers': ['general_file'],  # Пишем в общий лог
                'level': 'INFO',
                'propagate': True,  # Разрешаем передавать логи родительским логгерам
            },

            # Логгер для всего вашего приложения 'app'
            'app': {
                'handlers': ['general_file'],
                'level': 'INFO',
                'propagate': True,
            },

            # Логгер для админки
            'app.admin': {  # Все модули в папке admin
                'handlers': ['admin_file'],
                'level': 'INFO',
                'propagate': False,
            },

            # Логгер для сигналов:
            'app.signals': {
                'handlers': ['signals_file'],  # Пишем в отдельный файл
                'level': 'INFO',
                'propagate': False,  # Не передаем дальше, чтобы не дублировать
            },

            # Логгер для задачь Celery:
            'app.tasks_all': {
                'handlers': ['tasks_file'],
                'level': 'INFO',
                'propagate': False,
            },

            # Логгер для задачь Views:
            'app.views': {
                'handlers': ['views_file'],
                'level': 'INFO',
                'propagate': False,
            },

            # Логгер для задачь моделей db:
            'app.db_models': {
                'handlers': ['db_models'],
                'level': 'INFO',
                'propagate': False,
            },


        },

    }

    return data_loggers
