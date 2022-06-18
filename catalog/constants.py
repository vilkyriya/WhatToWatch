class CompositionTypes:
    NOT_DEFINED = 'not_defined'
    MOVIE = 'movie'
    SERIES = 'series'
    SHOW = 'show'

    CHOICES = (
        (NOT_DEFINED, 'Не выбрано',),
        (MOVIE, 'Фильм',),
        (SERIES, 'Сериал',),
        (SHOW, 'Шоу',),
    )


class CompositionStatuses:
    TO_WATCH = 'to_watch'
    IN_PROCESS = 'in_process'
    WATCHED = 'watched'

    CHOICES = (
        (TO_WATCH, 'Посмотреть',),
        (IN_PROCESS, 'В процессе',),
        (WATCHED, 'Завершён',),
    )
