from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.db import models
from django.shortcuts import reverse
from django.utils.functional import cached_property

from . import constants


class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Название', blank=True, null=True)
    slug = AutoSlugField(populate_from='name', blank=True, null=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        managed = True

    def __str__(self):
        return f'{self.slug}'


class Composition(models.Model):
    id_composition = models.AutoField(
        primary_key=True,
    )
    type = models.CharField(
        verbose_name="Тип",
        max_length=50,
        choices=constants.CompositionTypes.CHOICES,
        default=constants.CompositionTypes.NOT_DEFINED,
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название',
        default='',
    )
    name_eng = models.CharField(
        max_length=250,
        verbose_name='Английское название',
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        blank=True,
        null=True,
        unique=True,
    )

    # Это для сериалов и шоу
    season = models.IntegerField(
        verbose_name='Сезон',
        blank=True,
        null=True,
    )
    episodes = models.IntegerField(
        verbose_name='Эпизоды',
        blank=True,
        null=True,
    )
    last_watched = models.IntegerField(
        verbose_name='Последний просмотренный',
        blank=True,
        null=True,
    )

    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=False,
        null=False,
    )

    rating_my = models.FloatField(
        verbose_name='Мой рейтинг',
        default=0,
        blank=True,
        null=True,
    )

    url_info = models.CharField(
        max_length=100,
        verbose_name='Инфо',
        blank=True,
        null=True,
    )
    url_to_watch = models.CharField(
        max_length=100,
        verbose_name='Где посмотреть',
        blank=True,
        null=True,
    )

    id_group = models.ForeignKey(
        to=Group,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
        blank=True,
        null=True,
    )

    status = models.CharField(
        verbose_name="Статус",
        max_length=50,
        choices=constants.CompositionStatuses.CHOICES,
        default=constants.CompositionStatuses.TO_WATCH,
    )

    to_ignore = models.BooleanField(
        verbose_name='Игнорировать',
        default=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        managed = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.rating_my:
            self.rating_my = 0
        self.rating_my = str(self.rating_my)[:3]
        if not self.season:
            self.season = 0

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("composition", kwargs={
            'slug': self.slug
        })

    def get_absolute_url_v2(self):
        return reverse("composition-v2", args=[self.id_composition])

    @cached_property
    def full_name(self):
        if self.type != 'movie' and self.id_group:
            return f'{self.name} {self.season}, {self.year}'

        return f'{self.name}, {self.year}'

    @cached_property
    def full_name_eng(self):
        if self.type != 'movie' and self.id_group:
            return f'{self.name_eng} {self.season}'

        return self.name_eng

    @cached_property
    def progress(self):
        if self.type == 'movie':
            return None

        progress = int(self.last_watched / self.episodes * 100)
        return progress if progress >= 15 else 15

    def save(self, *args, **kwargs):
        from .utils import get_season

        if not self.season:
            self.season = get_season(self.type, self.year, self.id_group)

        if not self.slug:
            if self.type == "movie":
                self.slug = '-'.join((slugify(self.name_eng), slugify(self.year)))
            else:
                self.slug = '-'.join((slugify(self.name_eng), slugify(self.season), slugify(self.year)))

        if not self.episodes:
            self.episodes = 1

        if not self.last_watched:
            self.last_watched = 0
        super(Composition, self).save(*args, **kwargs)
