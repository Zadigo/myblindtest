from mcp_server import MCPToolset, ModelQueryToolset
from songs.models import Artist, Song
from mcp_server import mcp_server as mcp
from songs.choices import MusicGenre
from mcp.server.fastmcp import Context


class SongQueryTool(ModelQueryToolset):
    model = Song
    search_fields = [
        'name',
        'artist__name',
        'genre',
        'year',
        'difficulty',
        'created_on'
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('artist').all()


class ArtistQueryTool(ModelQueryToolset):
    model = Artist
    search_fields = [
        'name',
        'birthname',
        'date_of_birth',
        'spotify_id',
        'genre',
        'is_group',
        'wikipedia_page',
        'created_on'
    ]


class SongTools(MCPToolset):
    def create_song(self, name: str, artist: str, youtube_id: str, year: int = 2000, difficulty: int = 1) -> Song:
        """Create a new song with the given name and artist.

        Args:
            name (str): The name of the song.
            artist (str): The name of the artist.
            youtube_id (str): The YouTube ID of the song.
            year (int, optional): The year the song was released. Defaults to 2000.
            difficulty (int, optional): The difficulty level of the song. Defaults to 1.
        """
        artist, _ = Artist.objects.get_or_create(name=artist)
        song = Song.objects.create(
            name=name,
            artist=artist,
            youtube_id=youtube_id,
            year=year,
            difficulty=difficulty
        )
        return song

    def update_song(self, name: str, artist: str, youtube_id: str = None, year: int = None, difficulty: int = None) -> Song:
        """Update an existing song with the given name and artist.

        Args:
            name (str): The name of the song.
            artist (str): The name of the artist.
            youtube_id (str, optional): The new YouTube ID of the song. Defaults to None.
            year (int, optional): The new year the song was released. Defaults to None.
            difficulty (int, optional): The new difficulty level of the song. Defaults to None.
        """
        try:
            song = Song.objects.get(name=name, artist__name=artist)
        except Song.DoesNotExist:
            raise ValueError(f"Song '{name}' by '{artist}' does not exist.")
        else:
            if youtube_id is not None:
                song.youtube_id = youtube_id
            if year is not None:
                song.year = year
            if difficulty is not None:
                song.difficulty = difficulty

            song.save()
            return song


class ArtistTools(MCPToolset):
    def create_artist(self, name: str, birthname: str = None, date_of_birth: str = None, spotify_id: str = None, genre: str = None, is_group: bool = False, wikipedia_page: str = None) -> Artist:
        """Create a new artist with the given name and details.

        Args:
            name (str): The name of the artist.
            birthname (str, optional): The birth name of the artist. Defaults to None.
            date_of_birth (str, optional): The date of birth of the artist in YYYY-MM-DD format. Defaults to None.
            spotify_id (str, optional): The Spotify ID of the artist. Defaults to None.
            genre (str, optional): The genre of the artist. Defaults to None.
            is_group (bool, optional): Whether the artist is a group or not. Defaults to False.
            wikipedia_page (str, optional): The Wikipedia page URL of the artist. Defaults to None.
        """
        artist = Artist.objects.create(
            name=name,
            birthname=birthname,
            date_of_birth=date_of_birth,
            spotify_id=spotify_id,
            genre=genre,
            is_group=is_group,
            wikipedia_page=wikipedia_page
        )
        return artist

    def update_artist(self, name: str, birthname: str = None, date_of_birth: str = None, spotify_id: str = None, genre: str = None, is_group: bool = None, wikipedia_page: str = None) -> Artist:
        """Update an existing artist with the given name and details.

        Args:
            name (str): The name of the artist.
            birthname (str, optional): The new birth name of the artist. Defaults to None.
            date_of_birth (str, optional): The new date of birth of the artist in YYYY-MM-DD format. Defaults to None.
            spotify_id (str, optional): The new Spotify ID of the artist. Defaults to None.
            genre (str, optional): The new genre of the artist. Defaults to None.
            is_group (bool, optional): Whether the artist is a group or not. Defaults to None.
            wikipedia_page (str, optional): The new Wikipedia page URL of the artist. Defaults to None.
        """
        try:
            artist = Artist.objects.get(name=name)
        except Artist.DoesNotExist:
            raise ValueError(f"Artist '{name}' does not exist.")
        else:
            if birthname is not None:
                artist.birthname = birthname

            if date_of_birth is not None:
                artist.date_of_birth = date_of_birth

            if spotify_id is not None:
                artist.spotify_id = spotify_id

            if genre is not None:
                artist.genre = genre

            if is_group is not None:
                artist.is_group = is_group

            if wikipedia_page is not None:
                artist.wikipedia_page = wikipedia_page

            artist.save()
            return artist


@mcp.tool()
async def get_all_main_genres(context: Context) -> str:
    data = MusicGenre.read()
    items = sorted(data.keys())
    return f"""
    The main top genres that are available in the system are:
    {', '.join(items)}
    """


@mcp.tool()
async def get_all_genres(context: Context) -> str:
    items = map(lambda x: x[0], MusicGenre.choices())
    return f"""
    The main top genres that are available in the system are:
    {', '.join(items)}
    """
