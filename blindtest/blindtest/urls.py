from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular import views as drf_views
from graphene_django.views import GraphQLView
from oauth_dcr import views as oauth_dcr_views

from blindtest.schema import schema
from blindtest.views import HomePage, SearchPage

urlpatterns = [
    path(
        'graphql/',
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
        name='graphql'
    ),
    path(
        '__debug__/',
        include('debug_toolbar.urls')
    ),
    path(
        'api/schema/',
        drf_views.SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'api/schema/swagger-ui/',
        drf_views.SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        drf_views.SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
    path(
        'api/v1/songs/',
        include('songs.urls'),
    ),
    re_path(
        r'^search/$',
        SearchPage.as_view(),
        name='search'
    ),
    path(
        'o/',
        include(('oauth2_provider.urls', 'oauth2_provider'), namespace='oauth2_provider')
    ),
    path(
        'o/register/',
        oauth_dcr_views.DynamicClientRegistrationView.as_view(),
        name='oauth2_dcr'
    ),
    path(
        'agents/',
        include(('mcp_server.urls', 'mcp_server'), namespace='mcp_server')
    ),
    re_path(
        r'^$',
        HomePage.as_view(),
        name='home'
    ),
    path(
        'admin/',
        admin.site.urls
    )
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
