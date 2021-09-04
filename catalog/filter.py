import django_filters
from django import forms

from catalog.models import Composition


class MovieFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr="icontains", label="Название")
    name_eng = django_filters.CharFilter(field_name='name_eng', lookup_expr="icontains", label="Оригинальное название")

    STATUS_CHOICES = (
        ('to_watch', 'Посмотреть'),
        ('watched', 'Завершён'),
    )

    status = django_filters.ChoiceFilter(field_name='status', label="Статус", choices=STATUS_CHOICES)

    year__gte = django_filters.NumberFilter(field_name='year', lookup_expr='gte', label="Год",
                                            widget=forms.NumberInput)
    year__lte = django_filters.NumberFilter(field_name='year', lookup_expr='lte', label="",
                                            widget=forms.NumberInput)

    rating_my__gte = django_filters.NumberFilter(field_name='rating_my', lookup_expr='gte', label="Мой рейтинг",
                                                 widget=forms.NumberInput)
    rating_my__lte = django_filters.NumberFilter(field_name='rating_my', lookup_expr='lte', label="",
                                                 widget=forms.NumberInput)

    class Meta:
        model = Composition
        fields = []


class SeriesShowFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr="icontains", label="Название")
    name_eng = django_filters.CharFilter(field_name='name_eng', lookup_expr="icontains", label="Оригинальное название")

    STATUS_CHOICES = (
        ('to_watch', 'Посмотреть'),
        ('in_process', 'В процессе'),
        ('watched', 'Завершён'),
    )

    season = django_filters.NumberFilter(field_name='season', lookup_expr='iexact', label="Сезон",
                                         widget=forms.NumberInput)

    status = django_filters.ChoiceFilter(field_name='status', label="Статус", choices=STATUS_CHOICES)

    year__gte = django_filters.NumberFilter(field_name='year', lookup_expr='gte', label="Год",
                                            widget=forms.NumberInput)
    year__lte = django_filters.NumberFilter(field_name='year', lookup_expr='lte', label="",
                                            widget=forms.NumberInput)

    rating_my__gte = django_filters.NumberFilter(field_name='rating_my', lookup_expr='gte', label="Мой рейтинг",
                                                 widget=forms.NumberInput)
    rating_my__lte = django_filters.NumberFilter(field_name='rating_my', lookup_expr='lte', label="",
                                                 widget=forms.NumberInput)

    class Meta:
        model = Composition
        fields = []
