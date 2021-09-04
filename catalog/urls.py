from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('catalog/<str:type>/', login_required(CatalogPageView.as_view()), name='catalog'),
    path('composition/<slug:slug>/', login_required(CompositionView.as_view()), name='composition'),
    path('change-watched-episodes/<slug:slug>-<episode>/', login_required(change_watched_episodes),
         name='change-watched-episodes')
]
