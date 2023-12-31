# Generated by Django 4.2.2 on 2023-06-18 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_logo', models.ImageField(upload_to='pics')),
                ('level', models.CharField()),
                ('region', models.CharField()),
                ('name', models.CharField()),
                ('gender', models.CharField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField()),
                ('year', models.CharField()),
                ('fav_throw', models.CharField()),
                ('role', models.CharField()),
                ('number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('profile_img', models.ImageField(upload_to='pics')),
                ('team', models.CharField()),
            ],
        ),
    ]
