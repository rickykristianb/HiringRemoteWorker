from django.apps import AppConfig


class UserapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userApi'

    def ready(self) -> None:
        import userApi.signals
