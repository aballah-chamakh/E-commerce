from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Notification.consumers import NotificationConsumer
from .tokenmiddlware import TokenAuthMiddlewareStack
application = ProtocolTypeRouter({

    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
            path('order/<int:pk>/', NotificationConsumer),
        ])
    ),

})
