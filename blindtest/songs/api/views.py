from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import (Count, ExpressionWrapper, F, IntegerField, Max,
                              Min, Q, Sum)
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
    queryset = Artist.objects.all()
    serializer_class = serializers.ArtistSongSerializer
    pagination_class = BasePagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            return qs.filter(
                Q(name__icontains=search) |
                Q(song__name__icontains=search)
            )
        return qs


class CreateSongs(generics.GenericAPIView):
    """Endpoint used to created new songs
    in the database"""

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            data = [data]

        serializers_list: list[serializers.SongSerializer] = []
        for song_data in data:
            serializer = serializers.SongSerializer(data=song_data)
            if serializer.is_valid():
                serializers_list.append(serializer)
                continue

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
                    (
                        instance.artist.name,
                    ),
                    countdown=15
                )

                if not instance.artist.wikipedia_page:
                    tasks.wikipedia_information.apply_async(
                        (
                            instance.artist.id,
                        ),
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

    def get(self, request):
        genres = cache.get('genres', None)

        if genres is None:
            data = MusicGenre.choices()
            values = sorted([x[0] for x in data])
            cache.add('genres', values, (24 * 60))
        return Response(data=values, status=status.HTTP_200_OK)


class GameSettings(generics.GenericAPIView):
    queryset = Song.objects.all()
    permission_classes = []

    def get(self, request):
        qs = super().get_queryset()

        # Get the minimum and maximim decade
        # ranges for the frontend
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
