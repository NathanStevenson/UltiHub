from django.db import models

# Create your models here.

# team model
class Team(models.Model):
    team_logo = models.ImageField(upload_to='pics', default="pics/default_prof_pic.png")
    level = models.CharField()
    name = models.CharField()
    type = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    confirm_password = models.CharField()

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
        return str(self.id) + ": " + self.name 