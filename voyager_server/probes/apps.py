from django.apps import AppConfig


class ProbesConfig(AppConfig):
    name = "voyager_server.probes"
    verbose_name = "Probes"

    def ready(self):
        try:
            import voyager_server.probes.signals  # noqa F401
        except ImportError:
            pass
