from django.urls import path

from sensors.views import TelemetryRetrieveAPIView


urlpatterns = [
    path("fake-data/", TelemetryRetrieveAPIView.as_view(), name="telemetry"),
]
