from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from voyager_server.users.api.views import UserViewSet
from voyager_server.probes.api.views import ProbeResultViewSet, ProbeTargetViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("v1/probe-results", ProbeResultViewSet)
router.register("v1/probe-targets", ProbeTargetViewSet)

app_name = "api"
urlpatterns = router.urls
