import os

from django.test import TestCase
from player.models import RlTeam, RlMatch, RlPlayer, RlUser
from _datetime import datetime
from player.views import upload_replay_no_redirect
from django.test.client import RequestFactory


class UploadTests(TestCase):

    def test_parse_json(self):
        
        with open("replays/D67D93FE4AE4513A902AC089E8EF9871.replay", "rb") as binary_file:
            data = binary_file.read()
        
        request = RequestFactory().post('upload_replay_no_redirect', upfile=data)
        response = upload_replay_no_redirect(request)
        
        print (response)

