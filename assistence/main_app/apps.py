from django.apps import AppConfig


class MainAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main_app"

class SpeechAssistantConfig(AppConfig):
    name = 'main_app'
    verbose_name = 'Speech Assistant'
