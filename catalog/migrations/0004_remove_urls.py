from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0003_auto_20220618_1444'),
    ]


operations = [
    migrations.RemoveField(
        model_name='composition',
        name='url_kinopoisk',
    ),
    migrations.RemoveField(
        model_name='composition',
        name='url_doramatv',
    ),
]
