from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from hackaton_app.consumer import DashConsumer

websocket_urlPattern = [
    path('ws/polData/', DashConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlPattern))
})
