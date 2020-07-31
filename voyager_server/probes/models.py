from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from netfields import CidrAddressField, NetManager
import uuid


class PrefixInfo(models.Model):
    objects = NetManager()
    TYPE_CHOICES = ((1, "RIR"), (2, "PRIVATE"))

    asn = models.PositiveIntegerField(blank=True, null=True)
    prefix = CidrAddressField(unique=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=64)
    country_code = models.CharField(max_length=3)
    rir = models.CharField(max_length=16, blank=True, null=True)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.prefix)


class ProbeTarget(models.Model):
    TARGET_TYPES = (
        (1, "ICMP"),
        (2, "UDP"),
        (3, "TCP"),
    )
    destination = models.CharField(max_length=64, unique=True)
    interval = models.PositiveIntegerField()
    probe_count = models.PositiveIntegerField(default=10)
    type = models.PositiveSmallIntegerField(choices=TARGET_TYPES, default=2)

    def __str__(self):
        return self.destination


class Prober(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    targets = models.ManyToManyField(ProbeTarget)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="only 1 user per prober")
        ]

    def __str__(self):
        return self.name


class ProbeResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    probe = models.ForeignKey(Prober, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    target = models.CharField(max_length=64)


class ProbeHop(models.Model):
    ip = models.CharField(max_length=64, null=True)
    dns_name = models.CharField(max_length=128, null=True)
    response_time = models.PositiveIntegerField()
    ttl = models.PositiveIntegerField()
    responded = models.BooleanField()
    result = models.ForeignKey(ProbeResult, on_delete=models.CASCADE, related_name="hops")
    prefix = models.ForeignKey(PrefixInfo, on_delete=models.SET_NULL, null=True)
