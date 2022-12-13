from django.apps import AppConfig


class CustomerandsalesmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CustomerAndSalesManagement'

    def ready(self):
        import CustomerAndSalesManagement.signals
