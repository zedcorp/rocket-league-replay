from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from player.conf import PlayerConf
from player.parser.data.data_loader import load_data
from player.parser.parser.frames import get_frames
from player.parser.data.object_numbers import get_player_info

import sys, string, os
import copy
import json

settings = PlayerConf()

# default view
def index(request):
    return HttpResponse("retert")

def replay(request, file):
    fs = FileSystemStorage()
    file = open(os.path.join(fs.base_location, file) + '.replay.final.json','r')
    response = HttpResponse(content=file)      
    return response

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
          step = 30
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
              myframes[int(i/step - 1)]['cars'][car]['name'] = get_player_info()[car]['name']
          ####################################################################################
        
          file = open(os.path.join(fs.base_location, myfile.name) + '.final.json','w')
          encoded_str = json.dumps(myframes)
          file.write(encoded_str)
        
        return render(request, 'player/start.html', {
            'data_url' : 'replay/' + os.path.splitext(os.path.basename(os.path.join(fs.base_location, myfile.name)))[0]
        })
    return render(request, 'player/upload.html')