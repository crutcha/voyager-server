from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class ProbeTarget(models.Model):
    destination = models.CharField(max_length=64)
    interval = models.PositiveIntegerField()

    def __str__(self):
        return self.destination


class ProbeResult(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    target = models.CharField(max_length=64)


class ProbeHop(models.Model):
    hop = models.CharField(max_length=64)
    response_time = models.PositiveIntegerField()
    ttl = models.PositiveIntegerField()
    responded = models.BooleanField()
    result = models.ForeignKey(ProbeResult, on_delete=models.CASCADE, related_name="hops")


class Prober(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    targets = models.ManyToManyField(ProbeTarget)

    def __str__(self):
        return self.name
