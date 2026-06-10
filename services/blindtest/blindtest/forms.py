import datetime

from django import forms
from django.core.validators import URLValidator
from songs.choices import MusicGenre


class WikipediaValidator(URLValidator):
    def __call__(self, value):
        super().__call__(value)

        if 'wikipedia.org' not in value:
            raise forms.ValidationError("The URL must be a Wikipedia page.")


def max_date_of_birth():
    current_year = datetime.datetime.now().year
    min_year = current_year - 10
    return datetime.date(min_year, 1, 31).isoformat()


class NewSongForm(forms.Form):
    name = forms.CharField(
        max_length=255
    )
    artist = forms.CharField(
        max_length=255
    )
    wikipedia_page = forms.URLField(
        required=False,
        validators=[WikipediaValidator]
    )
    date_of_birth = forms.DateField(
        required=False,
        initial=datetime.date(1990, 1, 1),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'max': max_date_of_birth(),
                'value': datetime.date(1990, 1, 1).isoformat()
            }
        ),
    )
    year = forms.IntegerField(
        required=False,
        initial=datetime.datetime.now().year,
        widget=forms.NumberInput(
            attrs={
                'min': 1900,
                'max': datetime.datetime.now().year,
                'value': datetime.datetime.now().year
            }
        )
    )
    genre = forms.CharField(
        max_length=255,
        required=False,
        initial=MusicGenre.default('Pop'),
        widget=forms.Select(
            choices=MusicGenre.choices()
        )
    )
    youtube_id = forms.CharField(
        max_length=255,
        required=True
    )
    is_group = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput()
    )
