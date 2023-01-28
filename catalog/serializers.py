import math
import typing

from rest_framework import serializers

from .models import Composition


class CompositionRetrieveSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    name = serializers.CharField()
    name_eng = serializers.CharField()
    year = serializers.IntegerField()
    type = serializers.CharField()
    season = serializers.IntegerField()
    last_watched = serializers.IntegerField()
    slug = serializers.SlugField()
    episodes = serializers.IntegerField()
    url_info = serializers.CharField()
    url_to_watch = serializers.CharField()
    to_ignore = serializers.BooleanField()

    height = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    # rating_my = serializers.SerializerMethodField()
    # form = serializers.SerializerMethodField()

    class Meta:
        model = Composition
        fields = (
            'name', 'name_eng', 'full_name', 'year', 'type', 'season',
            'last_watched', 'slug', 'episodes', 'url_info', 'url_to_watch', 'to_ignore',
            'height', 'width', 'group',
            # 'rating_my',
        )

    @staticmethod
    def get_height(obj):
        height = []
        if obj.type in ('show', 'series'):
            for h in range(0, math.ceil(obj.episodes / 10)):
                height.append(h)

        return height

    @staticmethod
    def get_width(obj):
        width = []
        if obj.type in ('show', 'series'):
            for w in range(1, 11):
                width.append(w)

        return width

    def get_group(self, obj):
        group = tuple(self._get_group_qs(obj.id_group) if obj.id_group else [])

        return {
            'show': group[:5],
            'collapse': group[5:],
        }

    @staticmethod
    def _get_group_qs(id_group: int) -> typing.List[Composition]:
        return Composition.objects.filter(id_group=id_group).order_by('year')


class CompositionPartialUpdateSerializer:
    rating_my = serializers.FloatField(required=False)
    to_ignore = serializers.BooleanField(required=False)

    class Meta:
        model = Composition
        fields = (
            'to_ignore', 'rating_my'
        )
