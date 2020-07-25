import pytest
from django.test import RequestFactory
from voyager_server.users.models import User
from voyager_server.probes.models import ProbeTarget, Prober
from voyager_server.probes.api.views import ProbeTargetViewSet

pytestmark = pytest.mark.django_db


class TestProbeResultsViewSet:
    def test_post_results(self, rf: RequestFactory):
        test_result = {
            "dest": "8.8.8.8",
            "start_time": "2020-07-25T17:42:55.90005395-04:00",
            "end_time": "2020-07-25T17:43:18.412804618-04:00",
            "responses": [
                {
                    "probe_source": "",
                    "response_time": 0,
                    "ttl": 1,
                    "header_source": "",
                    "header_dest": "",
                },
                {
                    "probe_source": "192.168.10.1",
                    "response_time": 1,
                    "ttl": 1,
                    "header_source": "192.168.10.213",
                    "header_dest": "8.8.8.8",
                },
            ],
        }

    def test_probe_target_queryset(self, rf: RequestFactory):
        probe_user_1 = User.objects.create(username="probe-user-1")
        probe_user_2 = User.objects.create(username="probe-user-2")
        probe_user_3 = User.objects.create(username="probe-user-3")
        target_1 = ProbeTarget.objects.create(destination="1.1.1.1", interval=15)
        target_2 = ProbeTarget.objects.create(destination="8.8.8.8", interval=15)
        prober_1 = Prober.objects.create(user=probe_user_1)
        prober_2 = Prober.objects.create(user=probe_user_2)
        prober_3 = Prober.objects.create(user=probe_user_3)
        prober_1.targets.add(target_1)
        prober_2.targets.add(target_2)
        view = ProbeTargetViewSet.as_view({"get": "list"})
        request = rf.get("/api/v1/probes/probe-targets")

        request.user = probe_user_1
        view.request = request
        probe_1_response = view(request)

        assert len(probe_1_response.data) == 1
        assert probe_1_response.data[0]["destination"] == "1.1.1.1"

        request.user = probe_user_2
        view.request = request
        probe_2_response = view(request)

        assert len(probe_2_response.data) == 1
        assert probe_2_response.data[0]["destination"] == "8.8.8.8"

        request.user = probe_user_3
        view.request = request
        probe_3_response = view(request)

        assert len(probe_3_response.data) == 0
