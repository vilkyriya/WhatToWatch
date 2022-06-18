# Generated by Django 3.2 on 2022-06-18 14:44

from django.db import migrations, models
from django.db.models import F


def move_url_kinopoisk_to_url_info(apps, schema_editor):
    Composition = apps.get_model('catalog', 'Composition')

    Composition.objects.filter(url_kinopoisk__isnull=False).update(url_info=F('url_kinopoisk'))


def move_url_doramatv_to_url_to_watch(apps, schema_editor):
    Composition = apps.get_model('catalog', 'Composition')

    Composition.objects.filter(url_doramatv__isnull=False).update(url_to_watch=F('url_doramatv'))


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0002_auto_20220613_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='url_info',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Инфо'),
        ),
        migrations.AddField(
            model_name='composition',
            name='url_to_watch',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Где посмотреть'),
        ),
        migrations.RunPython(
            move_url_kinopoisk_to_url_info,
            migrations.RunPython.noop,
        ),
        migrations.RunPython(
            move_url_doramatv_to_url_to_watch,
            migrations.RunPython.noop,
        ),
    ]
