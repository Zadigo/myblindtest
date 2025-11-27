from flask import g
import graphene
from graphene_django import DjangoObjectType
from songs.models import Song, Artist
from graphene import relay
from songs import schema as song_schema


class ArtistType(DjangoObjectType):
    my_field = graphene.Boolean()

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

    def resolve_my_field(self, info):
        print(info)
        return True
        


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


class SongConnection(relay.Connection):
    class Meta:
        node = SongType


class Query(song_schema.TestQuery, graphene.ObjectType):
    paginate_songs = relay.ConnectionField(SongConnection)
    all_songs = graphene.List(SongType)
    song_by_id = graphene.Field(SongType, id=graphene.ID(required=True))
    filter_songs = graphene.List(SongType, name=graphene.String(), artist_name=graphene.String())

    # artist = relay.node.Field(ArtistType)
    all_artists = graphene.List(ArtistType)

    def resolve_paginate_songs(root, info, **kwargs):
        return Song.objects.select_related('artist').all()

    def resolve_all_songs(root, info):
        return Song.objects.select_related('artist').all()

    def resolve_all_artists(root, info):
        return Artist.objects.all()

    def resolve_song_by_id(root, info, id):
        return Song.objects.get(pk=id)
    
    def resolve_filter_songs(root, info, name=None, artist_name=None):
        queryset = Song.objects.select_related('artist').all()
        if name:
            queryset = queryset.filter(name=name)
        
        if artist_name:
            queryset = queryset.filter(artist__name__icontains=artist_name)
        
        return queryset


schema = graphene.Schema(query=Query)
