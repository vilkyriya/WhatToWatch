from django.contrib import admin

from catalog.models import Composition, Group


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    # add_form = CompositionAdminCreationForm
    # form = CompositionAdminChangeForm
    list_display = ['name', 'name_eng', 'year', 'type', 'season', 'rating_my']
    list_filter = ['status', 'type']
    list_editable = ['rating_my']
    search_fields = ['name', 'name_eng', 'slug']

    fieldsets = [
        ['Общие параметры', {
            'fields': ['type', 'name', 'name_eng', 'year', 'url_kinopoisk', 'url_doramatv', 'id_group', 'status']
        }],
        ['Параметры для сериалов и шоу', {
            'classes': ['collapse'],
            'fields': ['season', ('last_watched', 'episodes')],
        }],
        ['Параметры автоматические', {
            'classes': ['collapse'],
            'fields': ['slug', 'rating_my'],
        }],
    ]


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


admin.site.register(Group, GroupAdmin)
