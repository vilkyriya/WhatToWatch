from collections import Counter


def get_full_name(compositions):
    for composition in compositions:
        if composition.type == 'movie':
            composition.full_name = composition.name + ', ' + str(composition.year)
            composition.full_name_eng = composition.name_eng
            continue

        if composition.id_group is None:
            composition.full_name = composition.name + ', ' + str(composition.year)
            composition.full_name_eng = composition.name_eng
        else:
            composition.full_name = composition.name + ' ' + str(composition.season) + ', ' + str(composition.year)
            composition.full_name_eng = composition.name_eng + ' ' + str(composition.season)

    return compositions


def get_current_to_watch(compositions_to_watch, compositions_in_process=None):
    if compositions_in_process:
        groups_in_process = {composition.id_group for composition in compositions_in_process if composition.id_group}

        compositions_to_watch = compositions_to_watch.exclude(id_group__in=groups_in_process)

    unique_group_counter = Counter([composition.id_group for composition in compositions_to_watch
                                    if composition.id_group is not None])

    for group in unique_group_counter:
        if unique_group_counter[group] > 1:
            exclude_compositions = list(compositions_to_watch.filter(id_group=group).order_by('year'))[1:]
            for composition in exclude_compositions:
                compositions_to_watch = compositions_to_watch.exclude(
                    id_composition=composition.id_composition
                )

    return compositions_to_watch, compositions_in_process
