import graphene
from graphene_django import DjangoObjectType
from tvshows.models import TVShow, ThemeSong


class TVShowType(DjangoObjectType):
    class Meta:
        model = TVShow
        fields = '__all__'
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'title_fr': ['exact', 'icontains', 'istartswith'],
        }


class ThemeSongType(DjangoObjectType):
    youtube_url = graphene.String()

    class Meta:
        model = ThemeSong
        fields = '__all__'
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'series__title': ['exact', 'icontains', 'istartswith'],
        }

    def resolve_youtube_url(self, info):
        if self.youtube_id:
            return f'https://www.youtube.com/watch?v={self.youtube_id}'
        return None


class ThemeSongQuery(graphene.ObjectType):
    all_tv_shows = graphene.List(TVShowType)
    all_theme_songs = graphene.List(ThemeSongType)

    def resolve_all_tvshows(root, info, **kwargs):
        return TVShow.objects.all()

    def resolve_all_theme_songs(root, info, **kwargs):
        return ThemeSong.objects.all()
