import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from blogs.consumers import BlogEditorConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogapi.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(
            [
                path("blog/<int:blog_id>", BlogEditorConsumer.as_asgi()),
            ]
        ),
    }
)
