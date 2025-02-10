from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from songs.models import Song
from django.db.models.aggregates import Count


@method_decorator(cache_page(1 * 60), name='dispatch')
class HomePage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics = Song.objects.aggregate(
            song_count=Count('id')
        )
        context['statistics'] = statistics
        return context
