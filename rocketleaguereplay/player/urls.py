from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('users.json', views.users, name='users'),
    path('replay/<str:file>', views.replay, name='replay'),
    path('play/<str:file>', views.play, name='play')
]
