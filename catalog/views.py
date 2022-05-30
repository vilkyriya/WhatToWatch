from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from catalog.models import Composition
from .filter import MovieFilter, SeriesShowFilter
from .forms import CompositionForm
from .utils import *


class HomePageView(ListView):
    template_name = 'home.html'
    model = Composition

    def get_context_data(self, **kwargs):
        all = Composition.objects.order_by('year', 'name')

        all_to_watch = all.filter(status='to_watch')
        all_in_process = all.filter(status='in_process')
        all_to_watch, all_in_process = select_unique_to_watch(all_to_watch, all_in_process)

        movies_to_watch = all.filter(type='movie', status='to_watch')
        movies_to_watch, _ = select_unique_to_watch(movies_to_watch)

        series_to_watch = all.filter(type='series', status='to_watch')
        series_in_process = all.filter(type='series', status='in_process')
        series_to_watch, series_in_process = select_unique_to_watch(series_to_watch, series_in_process)

        shows_to_watch = all.filter(type='show', status='to_watch')
        shows_in_process = all.filter(type='show', status='in_process')
        shows_to_watch, shows_in_process = select_unique_to_watch(shows_to_watch, shows_in_process)

        context = {
            'all_to_watch': all_to_watch,
            'all_in_process': all_in_process,
            'movies_to_watch': movies_to_watch,
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
