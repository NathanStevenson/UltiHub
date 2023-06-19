from django.db import models

# Create your models here.

# team model
class Team(models.Model):
    team_logo = models.ImageField(upload_to='pics')
    level = models.CharField()
    region = models.CharField()
    name = models.CharField()
    gender = models.CharField()
    email = models.EmailField()
    password = models.CharField()

    def __str__(self):
        return self.name
    
# User model (stores all personal info)
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField()
    year = models.CharField()
    fav_throw = models.CharField()
    role = models.CharField()
    number = models.IntegerField()
    email = models.EmailField()
    profile_img = models.ImageField(upload_to='pics')
    team = models.CharField()

    def __str__(self):
        return self.id + ": " + self.name 