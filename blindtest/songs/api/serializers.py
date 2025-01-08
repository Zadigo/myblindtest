from songs import validators
from rest_framework import fields, serializers
from songs.models import Artist, Song


class ArtistSerializer(serializers.Serializer):
    id = fields.IntegerField()
    name = fields.CharField()
    created_on = fields.DateField()


class SongSerializer(serializers.Serializer):
    # artist = ArtistSerializer(read_only=True)
    id = fields.IntegerField(read_only=True)
    name = fields.CharField(max_length=255)
    genre = fields.CharField(max_length=100)
    artist = fields.CharField(max_length=255)
    youtube = fields.URLField(read_only=True)
    youtube_id = fields.CharField()
    year = fields.IntegerField(allow_null=True)
    spotify_id = fields.CharField(read_only=True)
    spotify_avatar = fields.URLField(read_only=True)
    video_id = fields.CharField(read_only=True)
    youtube_watch_link = fields.URLField(read_only=True)
    difficulty = fields.IntegerField(
        default=1, 
        validators=[validators.validate_difficulty]
    )
    created_on = fields.DateField(read_only=True)

    def create(self, validated_data):
        # TODO: Implement new create method
        # artist, state = Artist.objects.get_or_create(artist=validated_data['artist'])
        # artist.song_set.create(**{
        #     'name': validated_data['name'],
        #     'genre': validated_data['genre'],
        #     'year': validated_data['year'],
        #     'video_id': validated_data['video_id'],
        #     'difficulty': validated_data['difficulty']
        # })
        return Song.objects.create(**validated_data)
