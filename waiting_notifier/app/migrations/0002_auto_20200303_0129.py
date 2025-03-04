# Generated by Django 3.0.3 on 2020-03-02 16:29
from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'app/fixture/reservationSlot.json', app_label='app')


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
