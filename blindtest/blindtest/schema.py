import graphene
from songs import schema as song_schema


class Query(song_schema.SongQuery, song_schema.ArtistQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
