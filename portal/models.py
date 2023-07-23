from django.db import models

# Create your models here.

# team model
class Team(models.Model):
    team_logo = models.ImageField(upload_to='pics', default="pics/default_prof_pic.png")
    level = models.CharField()
    # team name must be unique
    name = models.CharField(unique=True)
    type = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    confirm_password = models.CharField()

    # ManyToMany fields for interacting with other models

    # the reason we define User as a string is due to the nature of Python not being aware that User is defined
    # this is known as a lazy reference in Django community and allows circular referencing within models.
    players = models.ManyToManyField('User', related_name='players')
    admin = models.ManyToManyField('User', related_name='admin')

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

    # ManyToMany fields for interacting with other users
    teams_allowed = models.ManyToManyField(Team, related_name='teams_allowed')

    def __str__(self):
        return str(self.id) + ": " + self.name 