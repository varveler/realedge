from django.apps import AppConfig



class TradesConfig(AppConfig):
    name = 'trades'

    def ready(self):
        import trades.signals
