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
