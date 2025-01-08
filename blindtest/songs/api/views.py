from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.mixins import Response
from rest_framework.pagination import LimitOffsetPagination
from songs.api import serializers
from songs.choices import MusicGenre
from songs.models import Artist, Song


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

        # TODO: Use for now until we set the genres
        # on each artists
        search = self.request.GET.get('q')
        if search is not None:
            queryset = queryset.filter(artist__name__icontains=search)

        return queryset


class AllArtists(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = serializers.ArtistSerializer

    # TODO: Set the genres on each
    # artist  in the Artist model
    def get_queryset(self):
        queryset = cache.get('artists')
        if queryset is None:
            queryset = super().get_queryset()
            cache.set('artists', queryset, timeout=3600)

        search = self.request.GET.get('q')
        if search is not None:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class GetByArtist(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = serializers.ArtistSongSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            return qs.filter(
                Q(name__icontains =search) |
                Q(song__name__icontains=search)
            )
        return qs


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
            except IntegrityError as e:
                errors.append(e)
            except ValidationError as e:
                errors.append('Multiple artists returned')

        response_serializer = serializers.SongSerializer(
            instance=created_songs,
            many=True
        )

        template = {
            'errors': errors,
            'items': response_serializer.data
        }
        return Response(template, status=status.HTTP_201_CREATED)


class SongGenres(generics.GenericAPIView):
    def get(self, request):
        data = MusicGenre.choices()
        return Response(data=[x[0] for x in data])
