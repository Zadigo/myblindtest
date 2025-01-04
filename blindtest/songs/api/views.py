from rest_framework import generics, status
from rest_framework.mixins import Response
from songs.api import serializers
from songs.choices import MusicGenre
from songs.models import Song
from django.db import IntegrityError

class AllSongs(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = serializers.SongSerializer
    permission_classes = []


class RandomSong(generics.GenericAPIView):
    queryset = Song.objects.all()
    serializer_class = serializers.SongSerializer

    def get(self, request, *args, **kwargs):
        qs = super().get_queryset()
        return Response(data=qs)


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
