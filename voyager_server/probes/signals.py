from django.dispatch import receiver
from django.db.models.signals import post_save
from voyager_server.probes.models import ProbeResult
from voyager_server.probes.tasks import process_probe_result


@receiver(post_save, sender=ProbeResult)
def probe_result_post_save(sender, **kwargs):
    process_probe_result.delay(str(kwargs["instance"].id))
