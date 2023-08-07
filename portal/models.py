from django.db import models

# Create your models here.

# Event model (stores all team events in a organized manner)
class Event(models.Model):
    date = models.DateField()
    event_name = models.CharField()
    notes = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name
    
    
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
    players = models.ManyToManyField(User, related_name='players')
    admin = models.ManyToManyField(User, related_name='admin')

    # teams can have many events want the same structure
    team_events = models.ManyToManyField(Event)

    def __str__(self):
        return self.name