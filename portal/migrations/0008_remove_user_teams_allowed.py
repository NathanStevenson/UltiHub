# Generated by Django 4.2.2 on 2023-08-07 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_event_team_team_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='teams_allowed',
        ),
    ]