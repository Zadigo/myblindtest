from django.db import models
from django.db.models.aggregates import Count
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from songs import tasks
from songs.models import Artist, Song

from blindtest.forms import NewSongForm


# @method_decorator(cache_page(1 * 60), name='dispatch')
class HomePage(FormView):
    template_name = 'home.html'
    form_class = NewSongForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics = Song.objects.aggregate(song_count=Count('id'))
        context['statistics'] = statistics

        mode = self.request.GET.get('mode', None)
        if mode == 'create':
            context['defaults']['artist_name'] = self.request.GET.get('name', None)
            context['defaults']['artist_date_of_birth'] = self.request.GET.get('date_of_birth', None)
            context['defaults']['artist_is_group'] = self.request.GET.get('is_group', None)
            context['defaults']['artist_wikipedia_page'] = self.request.GET.get('wikipedia_page', None)
            context['defaults']['artist_genre'] = self.request.GET.get('genre', None)

        return context

    def form_valid(self, form: NewSongForm):
        response = super().form_valid(form)

        artist, _ = Artist.objects.get_or_create(
            defaults={
                'is_group': form.cleaned_data['is_group'],
                'date_of_birth': form.cleaned_data['date_of_birth'],
                'wikipedia_page': form.cleaned_data['wikipedia_page']
            },
            name=form.cleaned_data['artist']
        )

        Song.objects.get_or_create(
            defaults={
                'artist': artist,
                'year': form.cleaned_data['year'],
                'genre': form.cleaned_data['genre'],
                'youtube_id': form.cleaned_data['youtube_id']
            },
            name=form.cleaned_data['name']
        )

        tasks.artist_spotify_information.apply_async(
            args=[artist.name], countdown=5)
        tasks.wikipedia_information.apply_async(args=[artist.id], countdown=5)

        return response


class SearchPage(ListView):
    template_name = 'search.html'
    model = Song
    context_object_name = 'songs'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')

        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(artist__name__icontains=search)
            )

        return queryset
