from mcp_server import MCPToolset, ModelQueryToolset
from songs.models import Artist, Song


class SongQueryTool(ModelQueryToolset):
    model = Song

    def get_queryset(self):
        return super().get_queryset()


class ArtistQueryTool(ModelQueryToolset):
    model = Artist


class SongTools(MCPToolset):
    def create_song(self, name: str, artist: str) -> Song:
        artist, _ = Artist.objects.get_or_create(name=artist)
        song = Song.objects.create(
            name=name,
            artist=artist,
            youtube_id=None,
            year=2000,
            difficulty=1
        )
        return song
