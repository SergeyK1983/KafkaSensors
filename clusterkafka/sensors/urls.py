from django.urls import path

from sensors.views import TelemetryRetrieveAPIView, sender_telemetry

urlpatterns = [
    path("fake-data/", TelemetryRetrieveAPIView.as_view(), name="telemetry"),
    path("sender/", sender_telemetry, name="telemetry_sender"),
]
