from django.urls import path
from voyager_server.probes.views import ResultDetailView

app_name = "probes"
urlpatterns = [path("<str:pk>", view=ResultDetailView.as_view(), name="detail")]
