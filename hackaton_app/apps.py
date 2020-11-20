from django.apps import AppConfig


class HackatonAppConfig(AppConfig):
    name = 'hackaton_app'

    def ready(self):
        import hackaton_app.signals
