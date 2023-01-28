from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from rest_framework import mixins, viewsets

from .filter import MovieFilter, SeriesShowFilter
from .forms import CompositionForm
from .utils import *
from . import serializers


class HomePageView(ListView):
    template_name = 'home.html'
    model = Composition

    def get_context_data(self, **kwargs):
        compositions = Composition.objects.order_by('year', 'name')

        ignored = compositions.filter(to_ignore=True)
        ignored_to_watch = ignored.filter(status='to_watch')
        ignored_in_process = ignored.filter(status='in_process')
        ignored_to_watch, ignored_in_process = select_unique_to_watch(ignored_to_watch, ignored_in_process)

        compositions = compositions.filter(to_ignore=False)

        compositions_to_watch = compositions.filter(status='to_watch')
        compositions_in_process = compositions.filter(status='in_process')
        compositions_to_watch, compositions_in_process = select_unique_to_watch(
            compositions_to_watch, compositions_in_process,
        )

        movies_to_watch = compositions.filter(type='movie', status='to_watch')
        movies_to_watch, _ = select_unique_to_watch(movies_to_watch)

        series_to_watch = compositions.filter(type='series', status='to_watch')
        series_in_process = compositions.filter(type='series', status='in_process')
        series_to_watch, series_in_process = select_unique_to_watch(series_to_watch, series_in_process)

        shows_to_watch = compositions.filter(type='show', status='to_watch')
        shows_in_process = compositions.filter(type='show', status='in_process')
        shows_to_watch, shows_in_process = select_unique_to_watch(shows_to_watch, shows_in_process)

        context = {
            'compositions_to_watch': compositions_to_watch,
            'compositions_in_process': compositions_in_process,
            'movies_to_watch': movies_to_watch,
            'series_to_watch': series_to_watch,
            'series_in_process': series_in_process,
            'shows_to_watch': shows_to_watch,
            'shows_in_process': shows_in_process,
            'ignored_in_process': ignored_in_process,
            'ignored_to_watch': ignored_to_watch,
        }
        return context


class CatalogPageView(ListView):
    template_name = 'catalog.html'
    model = Composition
    paginate_by = 12

    def get_context_data(self, **kwargs):

        if self.kwargs['type'] == 'movie':
            filterset_class = MovieFilter
        elif self.kwargs['type'] == 'series' or self.kwargs['type'] == 'show':
            filterset_class = SeriesShowFilter
        else:
            messages.error(self.request, 'Такой страницы не существует')
            return redirect('home')

        seriesfilter = filterset_class(self.request.GET, queryset=Composition.objects.filter(type=self.kwargs['type']))

        paginator = Paginator(seriesfilter.qs.order_by('name'), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'compositions': page_obj, 'page_obj': page_obj, 'filter': seriesfilter, 'type': self.kwargs['type']}
        return context


class CompositionView(DetailView):
    model = Composition
    template_name = 'composition/composition.html'
    context_object_name = 'composition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        composition = context['object']
        form = CompositionForm(instance=composition)

        if composition.type == 'show' or composition.type == 'series':
            import math
            height = []
            for h in range(0, math.ceil(composition.episodes / 10)):
                height.append(h)

            width = []
            for w in range(1, 11):
                width.append(w)

            composition.height = height
            composition.width = width

        if composition.id_group:
            group = Composition.objects.filter(id_group=composition.id_group).order_by('year')
        else:
            group = []

        context = {
            'composition': composition,
            'form': form,
            'group_show': group[:5],
            'group_collapse': group[5:],
        }
        return context

    def post(self, *args, **kwargs):
        form = CompositionForm(self.request.POST or None)

        if not form.is_valid():
            messages.error(self.request, 'Ошибка. Попробуйте еще раз')
            return redirect('home')

        composition = get_object_or_404(Composition, slug=kwargs['slug'])

        try:
            composition.status = 'watched'
            composition.rating_my = form.cleaned_data.get('rating_my')
            composition.save()

        except IntegrityError:
            messages.warning(self.request, 'Ошибка. Попробуйте еще раз')
            return redirect('home')

        messages.success(self.request, f'Рейтинг "{composition.full_name}" обновлён')
        return redirect('composition', slug=kwargs['slug'])


def change_watched_episodes(request, **kwargs):
    composition = get_object_or_404(Composition, slug=kwargs['slug'])

    try:
        if int(composition.last_watched) == int(kwargs['episode']):
            composition.last_watched -= 1
        else:
            composition.last_watched = kwargs['episode']

        if int(composition.last_watched) < int(composition.episodes):
            composition.status = 'in_process'
        if int(composition.last_watched) == int(composition.episodes):
            composition.status = 'watched'
        if int(composition.last_watched) == 0:
            composition.status = 'to_watch'

        composition.save()

    except IntegrityError:
        messages.warning(request, 'Ошибка. Попробуйте еще раз')
        return redirect('home')

    messages.success(
        request,
        f'Последняя просмотренная серия "{composition.full_name}" обновлена на {composition.last_watched}',
    )
    return redirect('composition', slug=kwargs['slug'])


def change_to_ignored(request, **kwargs):
    composition = get_object_or_404(Composition, slug=kwargs['slug'])
    is_ignored = bool(int(kwargs['is_ignored']))

    if composition.to_ignore == is_ignored:
        return redirect('composition', slug=kwargs['slug'])

    try:
        composition.to_ignore = is_ignored
        composition.save()
    except IntegrityError:
        messages.warning(request, 'Ошибка. Попробуйте еще раз')
        return redirect('home')

    if is_ignored:
        message = 'Добавлено в игнорируемые'
    else:
        message = 'Удалено из игнорируемых'

    messages.success(request, message)
    return redirect('composition', slug=kwargs['slug'])


class CompositionViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Composition.objects.all()
    template_name = 'composition/composition_v2.html'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CompositionRetrieveSerializer
        if self.action == 'partial_update':
            return serializers.CompositionPartialUpdateSerializer
        raise Http404("Can't find action")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return render(request, self.template_name, serializer.data)

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
