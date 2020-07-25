from rest_framework import serializers
from .models import ProbeTarget, ProbeResult, ProbeHop, Prober


class ProberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prober
        fields = "__all__"


class ProbeTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbeTarget
        fields = "__all__"


class ProbeHopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbeHop
        fields = ["ip", "dns_name", "responded", "response_time", "ttl"]


class ProbeResultSerializer(serializers.ModelSerializer):
    hops = ProbeHopSerializer(many=True)
    probe = serializers.SerializerMethodField()

    class Meta:
        model = ProbeResult
        fields = ["id", "start_time", "end_time", "probe", "target", "hops"]

    def create(self, validated_data):
        try:
            probe = Prober.objects.get(user=self.context["request"].user)
        except Prober.DoesNotExist:
            raise serializers.ValidationError("unable to determine probe agent")

        hops = validated_data.pop("hops")
        result = ProbeResult.objects.create(probe=probe, **validated_data)
        for hop in hops:
            ProbeHop.objects.create(result=result, **hop)

        return result

    def get_probe(self, obj):
        if obj.probe:
            return obj.probe.name
