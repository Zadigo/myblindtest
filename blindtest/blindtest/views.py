from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class HomePage(TemplateView):
    template_name = 'home.html'
    