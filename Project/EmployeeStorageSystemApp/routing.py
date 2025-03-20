from django.urls import path
from EmployeeStorageSystemApp.consumers import EmployeeConsumer

print('✅ WebSocket Routing Loaded')

websocket_urlpatterns = [
    path("ws/employees/", EmployeeConsumer.as_asgi()),
]
