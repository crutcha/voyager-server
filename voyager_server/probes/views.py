from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from voyager_server.probes.models import ProbeResult
import json


class ResultDetailView(LoginRequiredMixin, View):
    model = ProbeResult

    def get(self, *args, **kwargs):
        result = ProbeResult.objects.get(pk=kwargs["pk"])

        # This probably isn't the most efficient, but for now we'll do 2 passes
        # through the results to create d3js friendly graph. O(2n), could be worse...
        data = {"nodes": [], "links": []}
        hop_map = []
        filtered_results = result.hops.distinct("ip", "ttl").order_by("ttl")
        for hop in filtered_results:
            if not hop.ip:
                hop.ip = ""
            data["nodes"].append({"id": hop.id, "name": hop.ip})
            if len(hop_map) <= hop.ttl - 1:
                hop_map.append({hop.ip: hop.id})
            else:
                if not hop.ip in hop_map[hop.ttl - 1]:
                    hop_map[hop.ttl - 1] = {hop.ip: hop.id}

        # Connect every downstream node in directed graph
        for index in range(0, len(hop_map) - 1):
            for from_ip, from_id in hop_map[index].items():
                for to_ip, to_id in hop_map[index + 1].items():
                    data["links"].append({"source": from_id, "target": to_id})

        return render(args[0], "probes/proberesult_detail.html", {"data": json.dumps(data)})
