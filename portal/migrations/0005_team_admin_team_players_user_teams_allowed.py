# Generated by Django 4.2.2 on 2023-07-22 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_alter_team_team_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='admin',
            field=models.ManyToManyField(related_name='admin', to='portal.user'),
        ),
        migrations.AddField(
            model_name='team',
            name='players',
            field=models.ManyToManyField(related_name='players', to='portal.user'),
        ),
        migrations.AddField(
            model_name='user',
            name='teams_allowed',
            field=models.ManyToManyField(related_name='teams_allowed', to='portal.team'),
        ),
    ]
