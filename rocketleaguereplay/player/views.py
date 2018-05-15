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
    users = RlUser.objects.all()
    son_serialized_objects = serializers.serialize("json", users)
    return HttpResponse(son_serialized_objects)

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
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        
        os.path.join(fs.base_location, myfile.name)
        
        if not os.path.isfile(os.path.join(fs.base_location, myfile.name) + '.final.json'):
        
          # .replay to .json
          print('.replay to .json conversion: ' + filename)
          os.system(settings.Rocket_League_Replay_Parser_EXE_Location  + " " + os.path.join(fs.base_location, myfile.name) + " > " + os.path.join(fs.base_location, myfile.name) + '.json')
          
          # parsin json
          print('light .json processing: ' + os.path.join(fs.base_location, myfile.name) + '.json')
          load_data(os.path.join(fs.base_location, myfile.name) + '.json')
    
        
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
      
          for i in range(0, len(frames), step):
            if( i > 0 ):
              myframes.append(copy.deepcopy(myframes[int(i/step - 1)]))
            
            myframes[int(i/step - 1)]['time'] = frames[i]['time']['real_replay_time']
            myframes[int(i/step - 1)]['scoreboard'] = frames[i]['scoreboard']
            myframes[int(i/step - 1)]['cars'] = frames[i]['cars']
            myframes[int(i/step - 1)]['ball'] = frames[i]['ball']
            
            for car in myframes[int(i/step - 1)]['cars']:
              myframes[int(i/step - 1)]['cars'][car]['name'] = player_info[car]['name']
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
            RlPlayer.objects.get_or_create(userid=user[0], 
                         idmatch = match[0],
                         name=player['Name'], 
                         assist = player['Assists'], 
                         goal = player['Goals'], 
                         saves = player['Saves'], 
                         platform = player['Platform']['Value'], 
                         team = player['Team'], 
                         shot = player['Shots'])

         
          file = open(os.path.join(fs.base_location, myfile.name) + '.final.json','w')
          encoded_str = json.dumps(myframes)
          file.write(encoded_str)
        
        return redirect('play/' + os.path.splitext(os.path.basename(os.path.join(fs.base_location, myfile.name)))[0])
        
    return render(request, 'player/upload.html')