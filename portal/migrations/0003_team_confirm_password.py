# Generated by Django 4.2.2 on 2023-07-06 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_rename_gender_team_type_remove_team_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='confirm_password',
            field=models.CharField(default=''),
            preserve_default=False,
        ),
    ]