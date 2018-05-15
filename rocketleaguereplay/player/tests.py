from django.test import TestCase

# Create your tests here.
from player.models import RlTeam, RlMatch, RlPlayer, RlUser
from _datetime import datetime


class DBTests(TestCase):

    def test_create_match(self):
        match = RlMatch.objects.create(
                      scoreblue = 1,
                      scorered = 0,
                      starttime = datetime.now(), 
                      duration = 1)


    def test_create_user(self):
        user = RlUser.objects.create(onlineid=13, name='test')

    def test_create_player(self):
        RlPlayer.objects.create(
                     onlineid = '1', 
                     name = 'test',
                     assist = 1, 
                     goal = 1, 
                     saves = 1, 
                     platform = 'steam', 
                     team = 1, 
                     shot = 1)