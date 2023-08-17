from django.db import models

# Create your models here.

# Event model (stores all team events in a organized manner)
class Event(models.Model):
    date = models.DateField()
    event_name = models.CharField()
    notes = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name
    
# model to allow teams to customize their portal with new features
class portalOptions(models.Model):
    # by default every team comes with team logistics and practice plans. You can also enable film room and the discussion board
    # in the future we will add new features to these panels that you can either allow or not
    name = models.CharField()

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
    profile_img = models.ImageField(upload_to='pics', blank=True)
    team = models.CharField()

    # have the player know which teams they are allowed to access in order to efficiently access them via the dropdown menu
    # team is in quotes because it has not been defined yet so this allows Django to have circular redundancies with models
    teams_allowed = models.ManyToManyField('Team', related_name='teams_allowed', blank=True)

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

    # ManyToMany fields for interacting with other models

    # the reason we define User as a string is due to the nature of Python not being aware that User is defined
    # this is known as a lazy reference in Django community and allows circular referencing within models.
    players = models.ManyToManyField(User, related_name='players', blank=True)
    admin = models.ManyToManyField(User, related_name='admin', blank=True)

    # teams can have many events want the same structure
    team_events = models.ManyToManyField(Event, blank=True)

    # allow individual teams to have custom portal control
    portal_options = models.ManyToManyField(portalOptions)

    def __str__(self):
        return self.name