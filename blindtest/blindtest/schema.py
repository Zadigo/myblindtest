import graphene
from songs import schema as song_schema
from tvshows import schema as tvshow_schema


class Query(song_schema.SongQuery, song_schema.ArtistQuery, tvshow_schema.ThemeSongQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
