from django.test import TestCase
from django.contrib.auth.models import User

from users.models import Team, Profile


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

    def test_login_success(self):
        """Personnel can log in with valid credentials"""
        login = self.client.login(username="assembly", password="test1234")
        self.assertTrue(login)

    def test_login_failure(self):
        """Invalid login fails"""
        login = self.client.login(username="assembly", password="wrongpass")
        self.assertFalse(login)