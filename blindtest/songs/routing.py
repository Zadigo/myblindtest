from django.urls.conf import re_path
from songs.consumers.admin import (IndividualBlindTestConsumer,
                                   TeamBlindTestConsumer)
from songs.consumers.smartphone import SmartphoneConsumer
from songs.consumers.television import TelevisionConsumer

websocket_urlpatterns = [
    re_path(
        r'^ws/buzzer/connect$',
        SmartphoneConsumer.as_asgi(),
        name='smartphone'
    ),
    re_path(
        r'^ws/tv/connect$',
        TelevisionConsumer.as_asgi(),
        name='television'
    ),
    re_path(
        r'^ws/songs/single-player$',
        IndividualBlindTestConsumer.as_asgi(),
        name='single-player'
    ),
    re_path(
        r'^ws/songs$',
        TeamBlindTestConsumer.as_asgi(),
        name='songs'
    )
]
