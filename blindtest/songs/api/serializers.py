from django.forms import ValidationError
from songs import validators
from rest_framework import fields, serializers
from songs.models import Artist


class ArtistSerializer(serializers.Serializer):
    id = fields.IntegerField()
    name = fields.CharField()
    spotify_id = fields.CharField()
    spotify_avatar = fields.CharField()
    genre = fields.CharField()
    created_on = fields.DateField()


class SongSerializer(serializers.Serializer):
    id = fields.IntegerField(read_only=True)
    name = fields.CharField(max_length=255)
    genre = fields.CharField(max_length=100)
    featured_artists = fields.CharField(allow_null=True)
    youtube = fields.URLField(read_only=True)
    youtube_id = fields.CharField()
    year = fields.IntegerField(allow_null=True)
    spotify_id = fields.CharField(read_only=True)
    spotify_avatar = fields.URLField(read_only=True)
    youtube_watch_link = fields.URLField(read_only=True)
    artist_name = fields.CharField(write_only=True)
    artist = ArtistSerializer(read_only=True)
    difficulty = fields.IntegerField(
        default=1,
        validators=[validators.validate_difficulty]
    )
    created_on = fields.DateField(read_only=True)

    def to_internal_value(self, data):
        value = data.get('featured_artists')
        if value == '':
            data['featured_artists'] = None
        return super().to_internal_value(data)

    def validate(self, attrs):
        featured_artists = attrs['featured_artists']

        if featured_artists:
            tokens = featured_artists.split(',')
            clean_tokens = (str(token).strip() for token in tokens)
            attrs['featured_artists'] = ','.join(clean_tokens)
        return attrs

    def create(self, validated_data):
        artist_name = validated_data['artist_name']
        qs = Artist.objects.filter(name__icontains=artist_name.lower())

        if qs.exists():
            try:
                artist = qs.get()
            except:
                raise ValidationError(
                    "Multiple artist with the "
                    "same name exists"
                )
        else:
            artist = Artist.objects.create(
                name=validated_data['artist_name'],
                genre=validated_data['genre']
            )

        return artist.song_set.create(**{
            'name': validated_data['name'],
            'genre': validated_data['genre'],
            'year': validated_data['year'],
            'youtube_id': validated_data['youtube_id'],
            'difficulty': validated_data['difficulty']
        })

        # artist, state = Artist.objects.get_or_create(artist=validated_data['artist'])
        # artist.song_set.create(**{
        #     'name': validated_data['name'],
        #     'genre': validated_data['genre'],
        #     'year': validated_data['year'],
        #     'video_id': validated_data['video_id'],
        #     'difficulty': validated_data['difficulty']
        # })
        # return Song.objects.create(**validated_data)


class ArtistSongSerializer(serializers.Serializer):
    id = fields.IntegerField()
    name = fields.CharField()
    song_set = SongSerializer(many=True)
