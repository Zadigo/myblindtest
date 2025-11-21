from django.forms import ValidationError
from rest_framework import fields, serializers
from songs import tasks, validators
from songs.models import Artist


class ArtistSerializer(serializers.Serializer):
    id = fields.IntegerField()
    name = fields.CharField()
    spotify_id = fields.CharField()
    spotify_avatar = fields.CharField()
    genre = fields.CharField()
    wikipedia_page = fields.URLField(allow_null=True)
    created_on = fields.DateField()


class SongSerializer(serializers.Serializer):
    id = fields.IntegerField(read_only=True)
    name = fields.CharField(max_length=255)
    genre = fields.CharField(max_length=100)
    featured_artists = fields.CharField(allow_null=True, write_only=True)
    youtube = fields.URLField(read_only=True)
    youtube_id = fields.CharField()
    year = fields.IntegerField(allow_null=True)
    youtube_watch_link = fields.URLField(read_only=True)
    artist_name = fields.CharField(write_only=True)
    artist = ArtistSerializer(read_only=True)
    difficulty = fields.IntegerField(
        default=1,
        validators=[validators.validate_difficulty]
    )
    is_group = fields.BooleanField(default=False)
    wikipedia_page = fields.URLField(allow_null=True)
    created_on = fields.DateField(read_only=True)

    def to_internal_value(self, data):
        value = data.get('featured_artists')
        if value == '' or value == []:
            data['featured_artists'] = None
        return super().to_internal_value(data)

    def validate(self, attrs):
        featured_artists = attrs.get('featured_artists')

        if featured_artists is not None:
            tokens = featured_artists.split(',')
            clean_tokens = (str(token).strip() for token in tokens)
            attrs['featured_artists'] = ','.join(clean_tokens)
        return attrs

    def create(self, validated_data):
        artist_name = validated_data['artist_name']

        # If there are featured artists, create
        # them in the database
        featured_artists = validated_data.get('featured_artists')
        if featured_artists and featured_artists != '':
            artists = featured_artists.split(',')
            for artist_name in artists:
                instance, created = Artist.objects.get_or_create(
                    defaults={'name': artist_name},
                    name=artist_name
                )
                if created:
                    tasks.artist_spotify_information.apply_async(
                        args=[instance.name],
                        countdown=40
                    )

        artist, created = Artist.objects.get_or_create(
            defaults={
                'name': artist_name,
                'genre': validated_data['genre'],
                'is_group': validated_data.get('is_group', False),
                'wikipedia_page': validated_data.get('wikipedia_page', None),
            },
            name=artist_name
        )

        return artist.song_set.create(**{
            'name': validated_data['name'],
            'genre': validated_data['genre'],
            'year': validated_data['year'],
            'youtube_id': validated_data['youtube_id'],
            'difficulty': validated_data['difficulty']
        })


class ArtistSongSerializer(serializers.Serializer):
    """Serializer used to return an artist
    with all their songs"""

    id = fields.IntegerField()
    name = fields.CharField()
    spotify_avatar = fields.URLField()
    song_set = SongSerializer(many=True)
    wikipedia_page = fields.URLField(allow_null=True)


class SongAutomationSerializer(serializers.Serializer):
    year = fields.IntegerField()

    def update(self, instance, validated_data):
        for key, value in validated_data:
            setattr(instance, key, value)
        instance.save()
        return instance


class ArtistAutomationSerializer(serializers.Serializer):
    id = fields.IntegerField(read_only=True)
    name = fields.CharField()
    birthname = fields.CharField(required=True, allow_null=True)
    date_of_birth = fields.CharField(required=True, allow_null=True)

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        skip_keys = ['name']
        for key, value in validated_data.items():
            if key in skip_keys:
                continue
            setattr(instance, key, value)
        instance.save()
        return instance
