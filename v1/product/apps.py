from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'v1.product'
    label = 'product'

    def ready(self):
        import v1.product.signals
