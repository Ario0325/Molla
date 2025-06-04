from django.apps import AppConfig

class ArticleModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ArticleModule'
    verbose_name = 'ماژول مقالات'
    def ready(self):
        import ArticleModule.signals