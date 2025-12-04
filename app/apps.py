from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.admin_registration
        import app.db_models
        # Импортируем signals здесь, чтобы они были зарегистрированы
        import app.db_models.post_processing  # <- сигнал
        app.db_models.post_processing.register_file_cleanup()