from django.db.models import Count
from mcp.server.fastmcp import Context
from mcp_server import MCPToolset, ModelQueryToolset
from mcp_server import mcp_server as mcp
from songs import tasks
from songs.api.serializers import ArtistSerializer, SongSerializer
from songs.choices import MusicGenre
from songs.models import Artist, Song


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
    def create_song(self, song_name: str, artist: str, youtube_id: str, year: int = 2000, difficulty: int = 1, is_group: bool = False) -> dict:
        """Create a new song with the given name and artist.

        Args:
            song_name (str): The name of the song.
            artist (str): The name of the artist.
            youtube_id (str): The YouTube ID of the song.
            year (int, optional): The year the song was released. Defaults to 2000.
            difficulty (int, optional): The difficulty level of the song. Defaults to 1.
            is_group (bool, optional): Whether the artist is a group or not. Defaults to False.

        Returns:
            dict: The serialized data of the created song.
        """
        artist, state = Artist.objects.get_or_create(name__iexact=artist)

        if state:
            tasks.artist_spotify_information.apply_async(
                args=[artist.name],
                countdown=5
            )

        song = Song.objects.create(
            name=song_name,
            artist=artist,
            youtube_id=youtube_id,
            year=year,
            difficulty=difficulty,
            is_group=is_group
        )
        return SongSerializer(song).data

    def update_song(self, song_name: str, artist: str, youtube_id: str = None, year: int = None, difficulty: int = None, is_group: bool = None) -> dict:
        """Update an existing song with the given name and artist.

        Args:
            song_name (str): The name of the song.
            artist (str): The name of the artist.
            youtube_id (str, optional): The new YouTube ID of the song. Defaults to None.
            year (int, optional): The new year the song was released. Defaults to None.
            difficulty (int, optional): The new difficulty level of the song. Defaults to None.
            is_group (bool, optional): Whether the artist is a group or not. Defaults to None.

        Returns:
            dict: The serialized data of the updated song.
        """
        try:
            song = Song.objects.get(name=song_name, artist__name=artist)
        except Song.DoesNotExist:
            raise ValueError(
                f"Song '{song_name}' by '{artist}' does not exist."
            )
        else:
            if youtube_id is not None:
                song.youtube_id = youtube_id

            if year is not None:
                song.year = year

            if difficulty is not None:
                song.difficulty = difficulty

            if is_group is not None:
                song.is_group = is_group

            song.save()
            return SongSerializer(song).data

    def get_number_of_songs(self) -> int:
        """Get the total number of songs in the database."""
        return Song.objects.count()

    def get_by_year(self, min_year: int = None, max_year: int = None, genre: str = None, artist: str = None) -> list[dict]:
        """Get songs by their release year.

        Args:
            min_year (int, optional): The minimum release year of the songs to filter by. Defaults to None.
            max_year (int, optional): The maximum release year of the songs to filter by. Defaults to None.
            genre (str, optional): The genre of the songs to filter by. Defaults to None.
            artist (str, optional): The name of the artist to filter by. Defaults to None.

        Returns:
            list[dict]: A list of songs that match the year the songs were released.
        """
        qs = Song.objects.select_related('artist').all()
        if genre is not None:
            qs = qs.filter(genre=genre)

        if artist is not None:
            qs = qs.filter(artist__name=artist)

        if min_year is not None:
            qs = qs.filter(year__gte=min_year)

        if max_year is not None:
            qs = qs.filter(year__lte=max_year)

        return SongSerializer(qs, many=True).data
    
    def get_by_difficulty(self, min_difficulty: int = None, max_difficulty: int = None, genre: str = None) -> list[dict]:
        """Get songs by their difficulty level.

        Args:
            min_difficulty (int, optional): The minimum difficulty level of the songs to filter by. Defaults to None.
            max_difficulty (int, optional): The maximum difficulty level of the songs to filter by. Defaults to None.
            genre (str, optional): The genre of the songs to filter by. Defaults to None.

        Returns:
            list[dict]: A list of songs that match the given difficulty level.
        """
        qs = Song.objects.select_related('artist').all()
        if genre is not None:
            qs = qs.filter(genre=genre)

        if min_difficulty is not None:
            qs = qs.filter(difficulty__gte=min_difficulty)

        if max_difficulty is not None:
            qs = qs.filter(difficulty__lte=max_difficulty)

        return SongSerializer(qs, many=True).data   


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

        Returns:
            Artist: The created artist object.
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

        Returns:
            Artist: The updated artist object.
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

    def get_number_of_artists(self) -> int:
        """Get the total number of artists in the database."""
        return Artist.objects.count()

    def get_songs_per_artist(self, artist_name: str = None) -> list[dict[str, str | int]]:
        """Get the number of songs for each artist in the database or for a
        specific artist if the name is provided.

        Args:
            artist_name (str, optional): The name of the artist to filter by. Defaults to None, which means all artists will be included.

        Returns:
            list[dict[str, str | int]]: A list of dictionaries with artist names as keys and the number of songs as values.
          """
        qs = Song.objects.select_related('artist')

        qs_values = qs.values('artist__name')
        qs_annoated = qs_values.annotate(number_of_songs=Count('name'))

        if artist_name is not None:
            return qs_annoated.filter(artist__name=artist_name)
        return qs_annoated.order_by('-number_of_songs')

    def get_by_astrological_sign(self, sign: str) -> list[dict]:
        """Get artists by their astrological sign.

        Args:
            sign (str): The astrological sign to filter by.

        Returns:
            list[dict]: A list of artists that match the given astrological sign.
        """
        qs = Artist.objects.all()
        values = list(filter(lambda x: x.astrological_sign == sign, qs))
        return ArtistSerializer(values, many=True).data

    def get_by_age(self, min_age: int = None, max_age: int = None, genre: str = None) -> list[dict]:
        """Get artists by their age.

        Args:
            min_age (int, optional): The minimum age of the artists to filter by. Defaults to None.
            max_age (int, optional): The maximum age of the artists to filter by. Defaults to None.
            genre (str, optional): The genre of the artists to filter by. Defaults to None.

        Returns:
            list[dict]: A list of artists that match the given age criteria.
        """
        qs = Artist.objects.all()
        if genre is not None:
            qs = qs.filter(genre=genre)

        age_not_none = filter(lambda x: x.age is not None, qs)

        if min_age is None and max_age is None:
            return []

        if min_age is not None:
            qs = filter(lambda x: x.age >= min_age, age_not_none)

        if max_age is not None:
            qs = filter(lambda x: x.age <= max_age, age_not_none)

        return ArtistSerializer(qs, many=True).data


@mcp.tool()
async def get_all_main_genres(context: Context) -> str:
    """Get all the main genres available in the system. The main
    genres are defined in the MusicGenre class and are used to classify
    artists and songs. A main genre is a high-level category that encompasses a wide 
    range of musical styles and subgenres. Examples of main genres include Rock, Pop, Hip-Hop, Jazz, 
    Classical, and many more. The main genres are used to provide a general classification for artists and songs, 
    and they can help users discover new music based on their preferences.

    Args:
        context (Context): The context of the MCP tool, which can be used to access additional information or perform actions.

    Returns:
        str: A string listing all the main genres available in the system.
    """
    data = MusicGenre.read()
    items = sorted(data.keys())
    return f"""
    The main top genres that are available in the system are:
    {', '.join(items)}
    """


@mcp.tool()
async def get_all_genres(context: Context) -> str:
    """Get all the genres available in the system. The genres are defined in the MusicGenre 
    class and are used to classify artists and songs. A genre is a specific category of music that 
    is characterized by a particular style, form, or content. Examples of genres include Rock, Pop, Hip-Hop, Jazz,
    Classical, and many more. The genres are used to provide a more specific classification for artists and songs, 
    and they can help users discover new music based on their preferences.

    Args:
        context (Context): The context of the MCP tool, which can be used to access additional information or perform actions.

    Returns:
        str: A string listing all the genres available in the system.
    """
    items = map(lambda x: x[0], MusicGenre.choices())
    return f"""
    The main top genres that are available in the system are:
    {', '.join(items)}
    """
