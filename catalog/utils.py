import typing

from django.db.models import QuerySet, Count

from catalog.models import Composition


def select_unique_to_watch(
        compositions_to_watch: QuerySet,
        compositions_in_process: typing.Optional[QuerySet] = None,
) -> typing.Tuple[QuerySet, QuerySet]:
    if compositions_in_process:
        groups_in_process = compositions_in_process.filter(id_group__isnull=False).values_list('id_group', flat=True)

        compositions_to_watch = compositions_to_watch.exclude(id_group__in=groups_in_process)

    unique_group_counter = compositions_to_watch.filter(
        id_group__isnull=False,
    ).values(
        'id_group',
    ).annotate(
        id_group_count=Count('id_group'),
    ).filter(
        id_group_count__gt=1,
    ).order_by()

    exclude_composition_ids = list()
    for group in unique_group_counter:
        exclude_composition_ids.extend(tuple(compositions_to_watch.filter(
            status='to_watch',
            id_group=group['id_group'],
        ).order_by(
            'year',
        ).values_list(
            'id_composition',
            flat=True,
        )[1:]))

    compositions_to_watch = compositions_to_watch.exclude(id_composition__in=exclude_composition_ids)

    return compositions_to_watch, compositions_in_process


def get_season(type, year, id_group):
    if type == "movie":
        return 0

    if not id_group:
        return 1

    compositions = Composition.objects.filter(id_group=id_group, year__lt=year).order_by('year')

    if len(compositions) == 0:
        return 1
    else:
        return compositions.last().season + 1
