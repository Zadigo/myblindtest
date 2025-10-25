from django.urls.conf import re_path
from songs import consumers

websocket_urlpatterns = [
    re_path(
        r'^ws/buzzer/connect$',
        consumers.SmartphoneConsumer.as_asgi(),
        name='smartphone'
    ),
    re_path(
        r'^ws/tv/connect$',
        consumers.TelevisionConsumer.as_asgi(),
        name='television'
    ),
    re_path(
        r'^ws/songs$',
        consumers.SongConsumer.as_asgi(),
        name='songs'
    )
]
