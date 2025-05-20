from django.urls import path

from sensors.views import TelemetryRetrieveAPIView, TelemetrySenderListCreateAPIView, three_telemetry, \
    sending_fake_telemetry, input_telemetry

urlpatterns = [
    path("fake-data/", TelemetryRetrieveAPIView.as_view(), name="telemetry"),
    path("sync-telemetry/", TelemetrySenderListCreateAPIView.as_view(), name="telemetry_sender_create"),
    path("three/", three_telemetry, name="three"),
    path("fake-data-send/", sending_fake_telemetry, name="fake_telemetry"),
    path("input-telemetry/", input_telemetry, name="telemetry_input"),
]
