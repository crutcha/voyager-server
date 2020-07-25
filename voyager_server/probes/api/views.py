from rest_framework import viewsets
from voyager_server.probes.models import ProbeTarget, ProbeResult, ProbeHop
from voyager_server.probes import serializers


class ProbeTargetViewSet(viewsets.ModelViewSet):
    queryset = ProbeTarget.objects.all()
    serializer_class = serializers.ProbeTargetSerializer


class ProbeResultViewSet(viewsets.ModelViewSet):
    queryset = ProbeResult.objects.all()
    serializer_class = serializers.ProbeResultSerializer


class ProbeHopViewSet(viewsets.ModelViewSet):
    queryset = ProbeHop.objects.all()
    serializer_class = serializers.ProbeHopSerializer
