# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.shortcuts import reverse
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify, slugify


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
    TYPE_CHOICES = (
        ('not_defined', 'Не выбрано'),
        ('movie', 'Фильм'),
        ('series', 'Сериал'),
        ('show', 'Шоу'),
    )

    STATUS_CHOICES = (
        ('to_watch', 'Посмотреть'),
        ('in_process', 'В процессе'),
        ('watched', 'Завершён'),
    )

    id_composition = models.AutoField(primary_key=True)

    type = models.CharField(
        verbose_name="Тип",
        max_length=50,
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES[0][0]
    )

    name = models.CharField(max_length=100, verbose_name='Название', default='')
    name_eng = models.CharField(max_length=100, verbose_name='Английское название', blank=False, null=False)

    slug = models.SlugField(blank=True, null=True)

    # Это для сериалов и шоу
    season = models.IntegerField(verbose_name='Сезон', blank=True, null=True)
    episodes = models.IntegerField(verbose_name='Эпизоды', blank=True, null=True)
    last_watched = models.IntegerField(verbose_name='Последний просмотренный', blank=True, null=True)

    year = models.IntegerField(verbose_name='Год выпуска', blank=False, null=False)

    rating_my = models.FloatField(verbose_name='Мой рейтинг', default=0, blank=True, null=True)

    url_kinopoisk = models.CharField(max_length=100, verbose_name='Кинопоиск', blank=True, null=True)
    url_doramatv = models.CharField(max_length=100, verbose_name='ДорамаТВ', blank=True, null=True)

    id_group = models.ForeignKey(Group, models.SET_NULL, verbose_name='Группа', blank=True, null=True)

    status = models.CharField(
        verbose_name="Статус",
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0]
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

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.type == "movie":
                self.slug = '-'.join((slugify(self.name_eng), slugify(self.year)))
            else:
                self.slug = '-'.join((slugify(self.name_eng), slugify(self.season), slugify(self.year)))
        super(Composition, self).save(*args, **kwargs)
