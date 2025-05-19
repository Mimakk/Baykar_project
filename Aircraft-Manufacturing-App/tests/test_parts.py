from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Team, Profile
from parts.models import Part
from aircrafts.models import Aircraft

class AircraftManufacturingTests(TestCase):
    def setUp(self):
        # Create teams
        self.wing_team = Team.objects.create(name="Wing Team")
        self.fuselage_team = Team.objects.create(name="Fuselage Team")
        self.tail_team = Team.objects.create(name="Tail Team")
        self.avionics_team = Team.objects.create(name="Avionics Team")
        self.assembly_team = Team.objects.create(name="Assembly Team")

        # Create users and profiles
        self.wing_user = User.objects.create_user(username="wing", password="test123")
        self.fuselage_user = User.objects.create_user(username="fuselage", password="test123")
        self.tail_user = User.objects.create_user(username="tail", password="test123")
        self.avionics_user = User.objects.create_user(username="avionics", password="test123")
        self.assembly_user = User.objects.create_user(username="assembly", password="test123")

        Profile.objects.create(user=self.wing_user, team=self.wing_team)
        Profile.objects.create(user=self.fuselage_user, team=self.fuselage_team)
        Profile.objects.create(user=self.tail_user, team=self.tail_team)
        Profile.objects.create(user=self.avionics_user, team=self.avionics_team)
        Profile.objects.create(user=self.assembly_user, team=self.assembly_team)

        # Create parts for TB2
        self.wing = Part.objects.create(name="TB2 Wing", part_type="Wing", aircraft_type="TB2", team=self.wing_team, stock_count=1)
        self.fuselage = Part.objects.create(name="TB2 Fuselage", part_type="Fuselage", aircraft_type="TB2", team=self.fuselage_team, stock_count=1)
        self.tail = Part.objects.create(name="TB2 Tail", part_type="Tail", aircraft_type="TB2", team=self.tail_team, stock_count=1)
        self.avionics = Part.objects.create(name="TB2 Avionics", part_type="Avionics", aircraft_type="TB2", team=self.avionics_team, stock_count=1)

    def test_part_assignment_correct_team(self):
        # Correct part-team association should work
        self.assertEqual(self.wing.team.name, "Wing Team")
        self.assertEqual(self.fuselage.team.name, "Fuselage Team")

    def test_part_used_flag(self):
        self.assertFalse(self.wing.used)
        self.wing.used = True
        self.wing.save()
        self.assertTrue(Part.objects.get(id=self.wing.id).used)

    def test_part_aircraft_type_validation(self):
        # Try using a TB2 part for a TB3 aircraft (this should fail in actual validation logic, here just setup)
        part = Part.objects.create(name="TB3 Wing", part_type="Wing", aircraft_type="TB3", team=self.wing_team)
        self.assertNotEqual(self.wing.aircraft_type, part.aircraft_type)

    def test_aircraft_assembly(self):
        # Simulate an aircraft being assembled using the parts
        aircraft = Aircraft.objects.create(
            name="TB2-01",
            aircraft_type="TB2",
            wing=self.wing,
            fuselage=self.fuselage,
            tail=self.tail,
            avionics=self.avionics,
            assembled_by=self.assembly_user
        )

        # Mark parts as used
        for part in [self.wing, self.fuselage, self.tail, self.avionics]:
            part.used = True
            part.stock_count -= 1
            part.save()

        self.assertEqual(aircraft.aircraft_type, "TB2")
        self.assertTrue(all([Part.objects.get(id=part.id).used for part in [self.wing, self.fuselage, self.tail, self.avionics]]))

    def test_part_stock_decreases(self):
        stock_before = self.wing.stock_count
        self.wing.stock_count -= 1
        self.wing.save()
        self.assertEqual(self.wing.stock_count, stock_before - 1)

