from rest_framework import fields, serializers
from songs.models import Song


class SongSerializer(serializers.Serializer):
    id = fields.IntegerField(read_only=True)
    name = fields.CharField(max_length=255)
    genre = fields.CharField(max_length=100)
    artist = fields.CharField(max_length=255)
    youtube = fields.URLField()
    year = fields.IntegerField(allow_null=True)
    video_id = fields.CharField(read_only=True)
    youtube_watch_link = fields.URLField(read_only=True)
    difficulty = fields.IntegerField(read_only=True)
    created_on = fields.DateField(read_only=True)

    def create(self, validated_data):
        return Song.objects.create(**validated_data)
