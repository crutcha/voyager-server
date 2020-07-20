from django.db import models

# Create your models here.
class ProbeTarget(models.Model):
    destination = models.CharField(max_length=64)
    interval = models.PositiveIntegerField()


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
    result = models.ForeignKey(
        ProbeResult, on_delete=models.CASCADE, related_name="hops"
    )
