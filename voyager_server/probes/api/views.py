from rest_framework import viewsets
from voyager_server.probes.models import ProbeTarget, ProbeResult, ProbeHop
from voyager_server.probes import serializers
from rest_framework.permissions import IsAuthenticated

class ProbeTargetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProbeTarget.objects.all()
    serializer_class = serializers.ProbeTargetSerializer

    def get_queryset(self):
        return ProbeTarget.objects.filter(prober__user__id=self.request.user.id)


class ProbeResultViewSet(viewsets.ModelViewSet):
    queryset = ProbeResult.objects.all()
    serializer_class = serializers.ProbeResultSerializer


class ProbeHopViewSet(viewsets.ModelViewSet):
    queryset = ProbeHop.objects.all()
    serializer_class = serializers.ProbeHopSerializer
