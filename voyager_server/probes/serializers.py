from rest_framework import serializers
from .models import ProbeTarget, ProbeResult, ProbeHop


class ProbeTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbeTarget
        fields = "__all__"


class ProbeHopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbeHop
        fields = "__all__"


class ProbeResultSerializer(serializers.ModelSerializer):
    hops = ProbeHopSerializer(many=True)

    class Meta:
        model = ProbeResult
        fields = ["uuid", "start_time", "end_time", "target", "hops"]
