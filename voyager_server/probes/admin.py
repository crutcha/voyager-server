from django.contrib import admin
from voyager_server.probes import models


@admin.register(models.ProbeTarget)
class ProbeTargetAdmin(admin.ModelAdmin):
    list_display = ["destination", "interval"]


@admin.register(models.Prober)
class ProberAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]


@admin.register(models.ProbeHop)
class ProbeHopAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProbeResult)
class ProbeResultAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PrefixInfo)
class PrefixInfoAdmin(admin.ModelAdmin):
    list_display = ["prefix", "type", "asn", "name", "description"]
