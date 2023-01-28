from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *


urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('catalog/<str:type>/', login_required(CatalogPageView.as_view()), name='catalog'),
    path('composition/<slug:slug>/', login_required(CompositionView.as_view()), name='composition'),
    path(
        'change-watched-episodes/<slug:slug>-<episode>/',
        login_required(change_watched_episodes),
        name='change-watched-episodes',
    ),
    path(
        'change-to-ignored/<slug:slug>-<is_ignored>/',
        login_required(change_to_ignored),
        name='change-to-ignored',
    ),
    path(
        'composition_v2/<int:pk>',
        CompositionViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='composition-v2',
    ),
]
