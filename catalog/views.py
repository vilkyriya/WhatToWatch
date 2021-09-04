from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView, ListView, DetailView
from django_filters.views import FilterView
from catalog.models import Composition, Group
from django.shortcuts import redirect

from .filter import MovieFilter, SeriesShowFilter
from .forms import CompositionForm

from django.contrib import messages

from django.db import IntegrityError

import math

from .utils import get_full_name, get_current_to_watch


class HomePageView(ListView):
    template_name = 'home.html'
    model = Composition

    def get_context_data(self, **kwargs):
        movies_to_watch = Composition.objects.filter(type='movie', status='to_watch').order_by('?')
        movies_to_watch, _ = get_current_to_watch(movies_to_watch)
        movies_to_watch = get_full_name(movies_to_watch)

        series_to_watch = Composition.objects.filter(type='series', status='to_watch').order_by('?')
        series_in_process = Composition.objects.filter(type='series', status='in_process').order_by('?')
        series_to_watch, series_in_process = get_current_to_watch(series_to_watch, series_in_process)
        series_to_watch = get_full_name(series_to_watch)
        series_in_process = get_full_name(series_in_process)

        shows_to_watch = Composition.objects.filter(type='show', status='to_watch').order_by('?')
        shows_in_process = Composition.objects.filter(type='show', status='in_process').order_by('?')
        shows_to_watch, shows_in_process = get_current_to_watch(shows_to_watch, shows_in_process)
        shows_to_watch = get_full_name(shows_to_watch)
        shows_in_process = get_full_name(shows_in_process)

        context = {'movies_to_watch': movies_to_watch,
                   'series_to_watch': series_to_watch,
                   'series_in_process': series_in_process,
                   'shows_to_watch': shows_to_watch,
                   'shows_in_process': shows_in_process,
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
        page_obj = get_full_name(page_obj)

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
            group = get_full_name(group)
        else:
            group = []

        composition = get_full_name([composition, ])[0]

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

        if composition.type == 'movie':
            messages.success(self.request, f'Рейтинг "{composition}" обновлён')
        else:
            messages.success(self.request, f'Рейтинг "{composition} {composition.season}" обновлён')
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

    messages.success(request, f'Последняя просмотренная серия "{composition} {composition.season}" обновлена')
    return redirect('composition', slug=kwargs['slug'])
