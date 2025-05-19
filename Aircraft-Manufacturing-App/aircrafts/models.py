from django.db import models
from parts.models import Part
from django.contrib.auth.models import User

class Aircraft(models.Model):
    AIRCRAFT_TYPES = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA'),
    ]
    
    aircreaft_type = models.CharField(max_length=20, choices=AIRCRAFT_TYPES)
    
    wing = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='used_as_wing')
    fuselage = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='used_as_fuselage')
    tail = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='used_as_tail')
    avionics = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='used_as_avionics')

    assembled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assembled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.aircraft_type})"