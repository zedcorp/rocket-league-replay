from django.urls import path
from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('exists/<str:replay_id>', csrf_exempt(views.exists), name='exists'),
    path('upload_no_redirect', csrf_exempt(views.upload_no_redirect), name='upload_no_redirect'),
    path('users.json', views.users, name='users'),
    path('matchs.json', views.matchs, name='matchs'),
    path('replay/<str:file>', views.replay, name='replay'),
    path('play/<str:file>', views.play, name='play')
]
