from django.urls import path

from sensors.views import TelemetryRetrieveAPIView, sender_telemetry, TelemetrySenderListCreateAPIView, three_telemetry

urlpatterns = [
    path("fake-data/", TelemetryRetrieveAPIView.as_view(), name="telemetry"),
    path("sync-telemetry/", TelemetrySenderListCreateAPIView.as_view(), name="telemetry_sender_create"),
    path("sender/", sender_telemetry, name="telemetry_sender"),
    path("three/", three_telemetry, name="three"),

]
