from django.contrib.auth.models import User
from django.db import models

TEAMS = [
    ('Wing Team', 'Wing Team'),
    ('Fuselage Team', 'Fuselage Team'),
    ('Tail Team', 'Tail Team'),
    ('Avionics Team', 'Avionics Team'),
    ('Assembly Team', 'Assembly Team'),
]

class Team(models.Model):
    name = models.CharField(max_length=20,choices=TEAMS)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.team.name}"