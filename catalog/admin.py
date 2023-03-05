from django.contrib import admin
from django.utils.html import format_html

from catalog.models import Composition, Group


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_eng', 'year', 'type', 'season', 'rating_my', 'get_absolute_url',)
    list_filter = ('status', 'type', 'to_ignore',)
    list_editable = ('rating_my',)
    search_fields = ('name', 'name_eng', 'slug',)
    raw_id_fields = ('id_group',)
    readonly_fields = ('get_absolute_url',)

    fieldsets = (
        ('Общие параметры', {
            'fields': (
                'type', 'name', 'name_eng', 'year', 'url_info', 'url_to_watch', 'id_group', 'status', 'to_ignore',
            )
        }),
        ('Параметры для сериалов и шоу', {
            'classes': ('collapse',),
            'fields': ('season', ('last_watched', 'episodes',)),
        }),
        ('Параметры автоматические', {
            'classes': ('collapse',),
            'fields': ('slug', 'rating_my',),
        }),
    )

    @admin.display(
        description='Посмотреть на сайте',
    )
    def get_absolute_url(self, instance):
        if instance.pk:
            return format_html(
                "<a href='{url}'>Ссылка</a>",
                url=f'http://127.0.0.1:8000{instance.get_absolute_url()}',
            )
        else:
            return None


class CompositionInline(admin.TabularInline):
    model = Composition
    fields = ('name', 'name_eng', 'season', 'year', 'type',)
    raw_id_fields = ('id_group',)
    extra = 0
    ordering = ('year', 'season',)

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    inlines = (CompositionInline,)


admin.site.register(Group, GroupAdmin)
