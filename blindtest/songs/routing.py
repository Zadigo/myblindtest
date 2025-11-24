from django.urls.conf import re_path
from songs.consumers.admin import AdminConsumer
from songs.consumers.smartphone import PlayerConsumer
from songs.consumers.television import TelevisionConsumer

websocket_urlpatterns = [
    re_path(
        r'^ws/single-player/(?P<firebase>[a-zA-Z0-9]+)/connect$',
        PlayerConsumer.as_asgi(),
        name='smartphone'
    ),
    re_path(
        r'^ws/songs/(?P<firebase>[a-zA-Z0-9]+)/single-player$',
        AdminConsumer.as_asgi(),
        name='single-player'
    ),

    re_path(
        r'^ws/tv/connect$',
        TelevisionConsumer.as_asgi(),
        name='television'
    )
]
