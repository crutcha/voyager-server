from django.contrib import admin
from voyager_server.probes import models


@admin.register(models.ProbeTarget)
class ProbeTargetAdmin(admin.ModelAdmin):
    list_display = ["destination", "interval"]


@admin.register(models.Prober)
class ProberAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
