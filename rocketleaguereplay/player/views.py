from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core import serializers

from player.conf import PlayerConf
from player.parser.data.data_loader import load_data
from player.parser.parser.frames import get_frames, get_stats
from player.parser.data.object_numbers import get_player_info

from player.models import RlTeam, RlMatch, RlPlayer, RlUser

import sys, string, os
import copy
import json

settings = PlayerConf()

# default view
def index(request):
  
    return render(request, 'player/userlist.html')


def users(request):
    users = RlUser.objects.all().order_by('-nbmatchs')
    
    data = []

    for user in users:
      data.append({
        'id': user.id,
        'name': user.name,
        'nbmatchs': user.nbmatchs,
        'nbwin': user.nbwin,
        'nblose': user.nblose,
        'pwin': user.pwin,
        'pscore': user.score / user.nbmatchs,
        'nbgoalpermatch': user.nbgoal / user.nbmatchs,
        'nbassistpermatch': user.nbassist / user.nbmatchs,
        'nbsavepermatch': user.nbsave / user.nbmatchs,
        'score': user.score,
        'nbgoal': user.nbgoal,
        'nbassist': user.nbassist,
        'nbsave': user.nbsave
        })
      
    usersDto = {'data': data}
    

    jsonData = json.dumps(usersDto)
    #jsonData = json_serialized_objects = serializers.serialize("json", users)
    return HttpResponse(jsonData)

def matchs(request):
    players = RlPlayer.objects.filter(userid = request.GET.get('userid'))
    
    data = []

    for player in players:
      matchs = RlMatch.objects.filter(id = player.idmatch_id)
      for match in matchs:
        data.append({
          'datetime': str(match.starttime),
          'name1': '0',
          'name2': '0',
          'score1': '0',
          'score2': '0'
        })
      
    usersDto = {'data': data}
    

    jsonData = json.dumps(usersDto)
    #jsonData = json_serialized_objects = serializers.serialize("json", users)
    return HttpResponse(jsonData)
  
def replay(request, file):
    fs = FileSystemStorage()
    file = open(os.path.join(fs.base_location, file) + '.replay.final.json','r')
    response = HttpResponse(content=file)      
    return response

def play(request, file):
  return render(request, 'player/start.html', {
    'data_url' : '../replay/' + file
  })

def upload(request):
    fs = FileSystemStorage()
    if request.method == 'POST' and request.FILES['files']:
      for file in request.FILES.getlist('files'):
        if os.path.isfile(os.path.join(fs.base_location, file.name) + '.final.json'):
          print(file.name + " : file already imported" )
          continue
        else:
          filename = fs.save(file.name, file)
          uploaded_file_url = fs.url(filename)
          
          os.path.join(fs.base_location, file.name)
        
          try:
            # .replay to .json
            print(file.name + " : .replay to .json conversion")
            os.system(settings.Rocket_League_Replay_Parser_EXE_Location  + " " + os.path.join(fs.base_location, file.name) + " > " + os.path.join(fs.base_location, file.name) + '.json')
            
            # parsin json
            print(file.name + " : .json processing")
            load_data(os.path.join(fs.base_location, file.name) + '.json')
          except (Exception):
            print(file.name + " : error parsing json" )
            continue
        
          ################# dirty part should change the load_data instead #################
          frames = get_frames()
          player_info = get_player_info()
          
          step = 1
          myframes = [len(frames)/step]
          myframes[0] = {
              'time': 0,
              'scoreboard': {
                  'team0': 0,
                  'team1': 0
              },
              'ball': {'loc': {'x': 0, 'y': 0, 'z': 0},
                       'rot': {'x': 0, 'y': 0, 'z': 0},
                       'sleep': True,
                       'last_hit': None},
              'cars': {}
          }
      
          ####################################################################################
         
          stats = get_stats()
          
          match = RlMatch.objects.get_or_create(
            scoreblue = stats['blueteamscore'],
            scorered = stats['redteamscore'],
            starttime = stats['starttime'],
            duration = stats['duration'],
            rlmatchid = stats['matchid'])
                    
          for player in stats['playerstats'][0]:
            user = RlUser.objects.get_or_create(onlineid=str(player['OnlineID']), name=player['Name'])
            
            if player['Team'] == 0 and match[0].scoreblue > match[0].scorered:
              user[0].nbwin = user[0].nbwin + 1
            elif player['Team'] == 1 and match[0].scoreblue < match[0].scorered:
              user[0].nbwin = user[0].nbwin + 1
            
            user[0].nbmatchs = user[0].nbmatchs + 1 
            
            user[0].nblose = user[0].nblose
            user[0].pwin = user[0].nbwin * 100 / user[0].nbmatchs
            user[0].nbgoal = user[0].nbgoal + player['Goals']
            user[0].nbassist = user[0].nbassist + player['Assists']
            user[0].nbsave = user[0].nbsave + player['Saves']
            user[0].score = user[0].score + player['Score']
            
            RlPlayer.objects.get_or_create(userid=user[0], 
                         idmatch = match[0],
                         name=player['Name'], 
                         score = player['Score'], 
                         assist = player['Assists'], 
                         goal = player['Goals'], 
                         saves = player['Saves'], 
                         platform = player['Platform']['Value'], 
                         team = player['Team'], 
                         shot = player['Shots'])
            
            user[0].save()

          for i in range(0, len(frames), step):
            if( i > 0 ):
              myframes.append(copy.deepcopy(myframes[int(i/step - 1)]))
            
            myframes[int(i/step - 1)]['time'] = frames[i]['time']['real_replay_time']
            myframes[int(i/step - 1)]['scoreboard'] = frames[i]['scoreboard']
            myframes[int(i/step - 1)]['cars'] = frames[i]['cars']
            myframes[int(i/step - 1)]['ball'] = frames[i]['ball']
            
            for car in myframes[int(i/step - 1)]['cars']:
              myframes[int(i/step - 1)]['cars'][car]['name'] = player_info[car]['name']
         
          filefinal = open(os.path.join(fs.base_location, file.name) + '.final.json','w')
          encoded_str = json.dumps(myframes)
          filefinal.write(encoded_str)
        
      return redirect('play/' + os.path.splitext(os.path.basename(os.path.join(fs.base_location, file.name)))[0])
        
    return render(request, 'player/upload.html')