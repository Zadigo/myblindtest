from django.core.cache import cache
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.mixins import Response
from songs.api import serializers
from songs.choices import MusicGenre
from songs.models import Song
from collections import defaultdict
from rest_framework.pagination import LimitOffsetPagination


class BasePagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class AllSongs(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = serializers.SongSerializer

    def get_queryset(self):
        queryset = cache.get('songs')
        if queryset is None:
            queryset = super().get_queryset()
            cache.set('songs', queryset, timeout=3600)

        search = self.request.GET.get('q')
        if search is not None:
            queryset = queryset.filter(artist__icontains=search)

        return queryset


class GetByArtist(generics.GenericAPIView):
    def get(self, request, **kwargs):
        qs = Song.objects.all()

        paginator = BasePagination()
        result = paginator.paginate_queryset(qs, request)

        serializer = serializers.SongSerializer(instance=result, many=True)

        artists = []
        seen = []
        data = defaultdict(list)

        for song in serializer.data:
            artist = {'name': song['artist'], 'avatar': song['spotify_avatar']}
            if not artist['name'] in seen:
                artists.append(artist)
                seen.append(artist['name'])

            songs = data[song['artist']]
            songs.append(song)

        template = {
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
            'artists': list(artists),
            'items': data
        }

        return Response(template)


class CreateSongs(generics.GenericAPIView):
    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            data = [data]

        serializers_list = []
        for song_data in data:
            serializer = serializers.SongSerializer(data=song_data)
            if serializer.is_valid():
                serializers_list.append(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        created_songs = []
        for serializer in serializers_list:
            try:
                created_songs.append(serializer.save())
            except IntegrityError:
                errors.append()

        response_serializer = serializers.SongSerializer(
            instance=created_songs,
            many=True
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class SongGenres(generics.GenericAPIView):
    def get(self, request):
        data = MusicGenre.choices()
        return Response(data=[x[0] for x in data])
