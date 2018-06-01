import os

from django.test import TestCase
from player.models import RlTeam, RlMatch, RlPlayer, RlUser
from _datetime import datetime
from player.views import upload_no_redirect
from django.test.client import RequestFactory


class UploadTests(TestCase):

    def test_parse_json(self):
        
        with open("replays/285CACBB4F4EAC0C8AF82FBE58671C3B.zip", "rb") as binary_file:
            data = binary_file.read()
        
        request = RequestFactory().post('upload_no_redirect', content_type='application/zip', data=data)
        response = upload_no_redirect(request)
        
        print (response)

