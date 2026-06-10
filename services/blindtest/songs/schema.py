import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from songs.models import Artist, PopSong, Song


class ArtistType(DjangoObjectType):
    genre = graphene.String()
    birthname = graphene.String()

    class Meta:
        model = Artist
        fields = '__all__'
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'birthname': ['exact', 'icontains'],
            'is_group': ['exact']
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return super().get_queryset(queryset, info)

    def resolve_genre(self, info):
        if self.genre == 'nan':
            return None

        if self.genre is not None:
            return str(self.genre)

        return None
    
    def resolve_birthname(self, info):
        if self.birthname == 'nan':
            return None

        if self.birthname is not None:
            return str(self.birthname)

        return None


class SongType(DjangoObjectType):
    class Meta:
        model = Song
        fields = '__all__'
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'artist__name': ['exact', 'icontains'],
            'difficulty': ['exact', 'lt', 'gt']
        }


class PopSongType(DjangoObjectType):
    class Meta:
        model = PopSong
        fields = '__all__'
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith']
        }


class SongConnection(relay.Connection):
    class Meta:
        node = SongType


class ArtistQuery(graphene.ObjectType):
    all_artists = graphene.List(ArtistType)

    def resolve_all_artists(root, info):
        return Artist.objects.all()


class SongQuery(graphene.ObjectType):
    all_songs = graphene.List(SongType)
    search_songs = graphene.List(
        SongType,
        name=graphene.String(
            description="Name of the song to search for"
        ),
        artist_name=graphene.String(
            description="Name of the artist to search for"
        ),
        year=graphene.Int(
            description="Year the song was released"
        ),
        difficulty=graphene.Int(
            description="Difficulty level of the song"
        )
    )

    paginate_songs = relay.ConnectionField(SongConnection)
    song_by_id = graphene.Field(SongType, id=graphene.ID(required=True))

    all_pop_songs = graphene.List(
        PopSongType,
        name=graphene.String(
            description="Name of the pop song to search for"
        )
    )

    def resolve_paginate_songs(root, info, **kwargs):
        return Song.objects.select_related('artist').all()

    def resolve_all_songs(root, info):
        return Song.objects.select_related('artist').all()

    def resolve_song_by_id(root, info, id):
        return Song.objects.get(pk=id)

    def resolve_filter_songs(root, info, name=None, artist_name=None, year=None, difficulty=None):
        queryset = Song.objects.select_related('artist').all()

        if name:
            queryset = queryset.filter(name=name)

        if artist_name:
            queryset = queryset.filter(artist__name__icontains=artist_name)

        if year:
            queryset = queryset.filter(year=year)

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        return queryset

    def resolve_search_songs(root, info, name=None, artist_name=None):
        queryset = Song.objects.select_related('artist').all()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if artist_name:
            queryset = queryset.filter(artist__name__icontains=artist_name)

        return queryset

    def resolve_all_pop_songs(root, info, name=None):
        queryset = PopSong.objects.select_related('artist').all()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
