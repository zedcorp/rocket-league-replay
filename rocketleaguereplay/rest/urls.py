from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('test', views.test, name='test'),
    path('list_players', views.list_players, name='list_players'),
    path('players/<str:id>', views.player, name='player'),
    path('replays', views.replays, name='replays'),
    path('replays/<str:match_id>', views.replay, name='replay'),
]
