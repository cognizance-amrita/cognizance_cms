# Generated by Django 3.1.4 on 2021-01-21 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0005_auto_20210121_2042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='streak',
            new_name='streaks',
        ),
    ]
