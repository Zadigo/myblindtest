from django.urls.conf import re_path
from songs import consumers

websocket_urlpatterns = [
    re_path(
        r'^ws/connect$',
        consumers.ScreenInterfaceConsumer.as_asgi(),
        name='screen_projection'
    ),
    re_path(
        r'^ws/songs$',
        consumers.SongConsumer.as_asgi(),
        name='songs'
    )
]
