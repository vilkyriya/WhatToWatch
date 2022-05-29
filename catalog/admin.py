from django.contrib import admin

from catalog.models import Composition, Group


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_eng', 'year', 'type', 'season', 'rating_my',)
    list_filter = ('status', 'type',)
    list_editable = ('rating_my',)
    search_fields = ('name', 'name_eng', 'slug',)
    raw_id_fields = ('id_group',)

    fieldsets = (
        ('Общие параметры', {
            'fields': ('type', 'name', 'name_eng', 'year', 'url_kinopoisk', 'url_doramatv', 'id_group', 'status',)
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


class CompositionInline(admin.TabularInline):
    model = Composition
    fields = ('name', 'name_eng', 'season', 'year', 'type',)
    raw_id_fields = ('id_group',)
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    inlines = (CompositionInline,)


admin.site.register(Group, GroupAdmin)
