from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from users.models import Team, Profile
from parts.models import Part
from aircrafts.models import Aircraft

class AircraftAppTests(TestCase):

    def setUp(self):
        # Teams
        self.assembly_team = Team.objects.create(name="Assembly Team")
        self.wing_team = Team.objects.create(name="Wing Team")

        # Users
        self.assembly_user = User.objects.create_user(username="assembly", password="test1234")
        Profile.objects.create(user=self.assembly_user, team=self.assembly_team)

        self.wing_user = User.objects.create_user(username="winger", password="test1234")
        self.wing_profile = Profile.objects.create(user=self.wing_user, team=self.wing_team)

        # Parts for TB2 aircraft
        self.part_wing = Part.objects.create(
            name="Wing-1", part_type="Wing", team=self.wing_team,
            aircraft_type="TB2", stock_count=1
        )
        self.part_fuselage = Part.objects.create(
            name="Fuselage-1", part_type="Fuselage", team=self.wing_team,
            aircraft_type="TB2", stock_count=1
        )
        self.part_tail = Part.objects.create(
            name="Tail-1", part_type="Tail", team=self.wing_team,
            aircraft_type="TB2", stock_count=1
        )
        self.part_avionics = Part.objects.create(
            name="Avionics-1", part_type="Avionics", team=self.wing_team,
            aircraft_type="TB2", stock_count=1
        )

        # Aircraft
        self.aircraft = Aircraft.objects.create(
            name="TB2-1", aircraft_type="TB2",
            wing=self.part_wing,
            fuselage=self.part_fuselage,
            tail=self.part_tail,
            avionics=self.part_avionics,
            assembled_by=self.assembly_user
        )
        
    def test_aircraft_list_visible_to_assembly_team(self):
        """Aircrafts should be visible to Assembly Team"""
        self.client.login(username="assembly", password="test1234")
        response = self.client.get(reverse("aircraft-list"))  # Use your view name here
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TB2-1")

    def test_part_deletion(self):
        """Unused parts can be deleted, used parts cannot"""
        self.client.login(username="winger", password="test1234")
        # Unused part
        unused_part = Part.objects.create(
            name="Unused-Wing", part_type="Wing", team=self.wing_team,
            aircraft_type="TB2", stock_count=1, used=False
        )
        response = self.client.delete(reverse("part-detail", args=[unused_part.id]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Part.objects.filter(id=unused_part.id).exists())

        # Used part
        self.part_wing.used = True
        self.part_wing.save()
        response = self.client.delete(reverse("part-detail", args=[self.part_wing.id]))
        self.assertEqual(response.status_code, 400)  # ValidationError expected
        self.assertTrue(Part.objects.filter(id=self.part_wing.id).exists())
