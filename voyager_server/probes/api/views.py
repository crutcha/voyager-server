from rest_framework import viewsets
from voyager_server.probes.models import ProbeTarget, ProbeResult, ProbeHop
from voyager_server.probes.api import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class ProbeTargetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProbeTarget.objects.all()
    serializer_class = serializers.ProbeTargetSerializer

    def get_queryset(self):
        return ProbeTarget.objects.filter(prober__user__id=self.request.user.id)


class ProbeResultViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProbeResult.objects.all()
    serializer_class = serializers.ProbeResultSerializer

    @action(detail=True)
    @renderer_classes([JSONRenderer])
    def jsgraph(self, request, pk=None):
        result = ProbeResult.objects.get(pk=pk)

        # This probably isn't the most efficient, but for now we'll do 2 passes
        # through the results to create d3js friendly graph. O(2n), could be worse...
        data = {"nodes": [], "edges": []}
        hop_map = []
        filtered_results = result.hops.distinct("ip", "ttl").order_by("ttl")
        for hop in filtered_results:
            if not hop.ip:
                hop.ip = ""
            data["nodes"].append({"id": hop.id, "label": hop.dns_name})
            if len(hop_map) <= hop.ttl - 1:
                hop_map.append({hop.ip: hop.id})
            else:
                if not hop.ip in hop_map[hop.ttl - 1]:
                    hop_map[hop.ttl - 1][hop.ip] = hop.id

        # Connect every downstream node in directed graph
        for index in range(0, len(hop_map) - 1):
            for from_ip, from_id in hop_map[index].items():
                for to_ip, to_id in hop_map[index + 1].items():
                    data["edges"].append({"from": from_id, "to": to_id})

        return Response(data)


class ProbeHopViewSet(viewsets.ModelViewSet):
    queryset = ProbeHop.objects.all()
    serializer_class = serializers.ProbeHopSerializer
