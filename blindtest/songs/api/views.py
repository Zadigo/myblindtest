import json
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import (Count, ExpressionWrapper, F, IntegerField, Max,
                              Min, Q, QuerySet, Sum)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.mixins import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from songs import tasks
from songs.api import serializers
from songs.choices import MusicGenre
from songs.models import Artist, Song


class BasePagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100

    def get_paginated_response(self, data):
        previous_link = urlparse(self.get_previous_link())
        next_link = urlparse(self.get_next_link())

        q1 = previous_link.query
        q2 = next_link.query

        previous = parse_qs(q1).get('offset')
        next = parse_qs(q2).get('offset')

        if previous:
            previous = int(previous[0])

        if next:
            next = int(next[0])

        return Response({
            'count': self.count,
            'previous': previous,
            'next': next,
            'results': data
        })


class AllSongs(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = serializers.SongSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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


class SearchSongsAndArtists(generics.ListAPIView):
    """Endpoint used to search songs and artists
    in the database"""

    queryset = Artist.objects.all()
    serializer_class = serializers.ArtistSongSerializer
    pagination_class = BasePagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()

        search = self.request.GET.get('q')
        if search:
            logic = Q(name__icontains=search)
            qs1 = qs.filter(logic).distinct()
            return qs1
        return qs


class CreateSongs(generics.GenericAPIView):
    """Endpoint used to created new songs
    in the database"""

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            data = [data]

        serializer_errors = []

        serializers_list: list[serializers.SongSerializer] = []
        for index, song_data in enumerate(data):
            serializer = serializers.SongSerializer(data=song_data)
            if serializer.is_valid():
                serializers_list.append(serializer)
                continue
            else:
                result = serializer.errors
                result['index'] = index
                serializer_errors.append(result)

        if serializer_errors:
            return Response(serializer_errors, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        created_songs: list[Song] = []
        for serializer in serializers_list:
            try:
                instance: Song = serializer.save()
                created_songs.append(instance)
            except IntegrityError as e:
                errors.append(e)
            except ValidationError as e:
                errors.append('Multiple artists returned')
            else:
                if instance.artist.spotify_id:
                    continue

                tasks.artist_spotify_information.apply_async(
                    args=[instance.artist.name],
                    countdown=10
                )

                if instance.artist.wikipedia_page:
                    tasks.wikipedia_information.apply_async(
                        args=[instance.artist.id],
                        countdown=20
                    )

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
    permission_classes = [AllowAny]

    def read_file(self) -> list[dict[str, str | list[dict[str, str]]]]:
        path = settings.MEDIA_PATH / 'genres.json'
        with open(path, mode='r', encoding='utf-8') as f:
            data = json.load(f)

            main_categories = data.keys()
            genres = []

            for category in main_categories:
                template = {'category': None, 'items': []}
                template['category'] = category
                template['items'] = list(
                    map(lambda x: {'label': x}, data[category]))
                genres.append(template)
            return genres

    def get(self, request):
        genres: list[dict[str, str | list[dict[str, str]]]
                     ] = cache.get('genres', {})

        if not genres:
            genres = self.read_file()
            cache.set('genres', genres, timeout=24 * 60 * 60)
        return Response(data=genres, status=status.HTTP_200_OK)


class GameSettings(generics.GenericAPIView):
    queryset = Song.objects.all()
    permission_classes = [AllowAny]

    def get(self, request):
        qs = super().get_queryset()

        # Get the minimum and maximim decade
        period = ExpressionWrapper(
            timezone.now().year - F('year'),
            output_field=IntegerField()
        )
        result = qs.filter(year__gt=0).annotate(period=period)
        period_range = result.aggregate(
            minimum=Min('period'),
            maximum=Max('period')
        )

        # Count by genre
        result = qs.values('genre')
        result1 = result.annotate(count=Count('genre'))
        distribution_by_genre = result1.order_by('genre')

        total_by_genre = distribution_by_genre.aggregate(all=Sum('count'))
        distribution_by_genre_list = list(distribution_by_genre)
        distribution_by_genre_list.insert(
            0, {'genre': 'All', 'count': total_by_genre['all']}
        )

        template = {
            'period': period_range,
            'count_by_genre': distribution_by_genre_list
        }
        return Response(template, status=status.HTTP_200_OK)


@api_view(http_method_names=['get'])
def test(request):
    from songs import tasks
    tasks.song_information_completion.s()
    return Response({'status': 'ok'})


class SongsUpdateAutomation(generics.UpdateAPIView):
    """Endpoint that can be used by webscrapper in order
    to automate the updates of the pieces of information
    of the songs in the database"""

    queryset = Song.objects.filter(year=0)
    serializer_class = serializers.SongAutomationSerializer
    permission_classes = []


class ArtistAutomation(generics.GenericAPIView):
    queryset = Artist.objects.filter(
        Q(birthname__isnull=True) |
        Q(date_of_birth__isnull=True)
    )
    serializer_class = serializers.ArtistAutomationSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        queryset = super().get_queryset()
        values = queryset.values('id', 'name', 'birthname', 'date_of_birth')
        return Response(values, status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):
        artist_id = request.data.get('id')
        artist = get_object_or_404(Artist, id=artist_id)

        serializer = self.get_serializer(
            instance=artist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SongStatistics(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Song.objects.all()

    def get_queryset(self) -> QuerySet[Song]:
        qs = cache.get('songs_for_statistics')
        if qs is not None:
            return qs
        queryset = super().get_queryset()
        cache.set('songs_for_statistics', queryset, timeout=3600)
        return queryset

    def get(self, request):
        qs = self.get_queryset()

        template = {
            'distribution_by_genre': {
                'labels': [],
                'data': []
            }
        }

        # Distribution by genre
        result = qs.values_list('genre')
        result1 = result.annotate(count=Count('genre'))
        distribution_by_genre = result1.order_by('count')
        template['distribution_by_genre']['labels'] = [item[0]
                                                       for item in distribution_by_genre]
        template['distribution_by_genre']['data'] = [item[1]
                                                     for item in distribution_by_genre]

        return Response(template, status=status.HTTP_200_OK)
