import copy
import json
import os
import zipfile
import traceback
import io
import subprocess
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from player.conf import PlayerConf
from player.models import RlMatch, RlPlayer, RlUser
from player.parser.data.data_loader import load_data
from player.parser.data.object_numbers import get_player_info
from player.parser.parser.frames import get_frames, get_stats
from player.parser.frames_builder import create_match
from player.parser.replay_data import Match

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
    # jsonData = json_serialized_objects = serializers.serialize("json", users)
    return HttpResponse(jsonData)


def matchs(request):

    userPlayers = RlPlayer.objects.filter(userid = request.GET.get('userid'))
    
    data = []
    
    for userPlayer in userPlayers:
      matchs = RlMatch.objects.filter(id = userPlayer.idmatch_id).values('id','rlmatchid','scoreblue','scorered','duration','starttime')
      for match in matchs:
        nameBlue = []
        nameRed = []
        for matchPlayer in RlPlayer.objects.filter(idmatch__id = match['id']):
          if matchPlayer.team == 0:
            nameBlue.append(matchPlayer.name)
          if matchPlayer.team == 1:
            nameRed.append(matchPlayer.name)
        
        win = (userPlayer.team == 0 and match['scoreblue'] > match['scorered']) or (userPlayer.team == 1 and match['scoreblue'] < match['scorered'])
        
        data.append({
          'datetime': match['starttime'].timestamp(),
          'name1': nameBlue,
          'name2': nameRed,
          'score1': match['scoreblue'],
          'score2': match['scorered'],
          'win' : win,
          'rlmatchid': match['rlmatchid']
        })
      

    usersDto = {'data': data}

    jsonData = json.dumps(usersDto)
    # jsonData = json_serialized_objects = serializers.serialize("json", users)
    return HttpResponse(jsonData)


def replay(request, file):
    print("REPLAY: " + file)
    match = RlMatch.objects.filter(rlmatchid = file)
    # print(match[0].replayjson)
    response = HttpResponse(content=match[0].replayjson)
    return response


def play(request, file):
    return render(request, 'player/start.html', {
        'data_url': '../replay/' + file
    })

def upload(request):
    fs = FileSystemStorage()
    if request.method == 'POST' and request.FILES['files']:
        for file in request.FILES.getlist('files'):
            rl_match_id = file.name.split('.')[0]
            match = RlMatch.objects.filter(rlmatchid = rl_match_id)
            if len(match) > 0:
                print(file.name + " : file already imported")
                continue
            else:
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)

                os.path.join(fs.base_location, file.name)

                try:
                    # .replay to .json
                    zip_ref = zipfile.ZipFile(os.path.join(fs.base_location, file.name), 'r')
                    zip_ref.extractall(fs.base_location)
                    zip_ref.close()
                    # parsing json
                    load_data(os.path.join(fs.base_location, rl_match_id + '.json'))
                except Exception as e:
                    print(rl_match_id + " : error parsing json")
                    print("OS error: {0}".format(e))
                    traceback.print_exc()
                    continue

                handle_json(fs, rl_match_id)

        return redirect('play/' + rl_match_id)

    return render(request, 'player/upload.html')


def exists(request, replay_id):
    matchs = RlMatch.objects.filter(rlmatchid=replay_id)
    status = 200 if (len(matchs) > 0 and matchs[0].replayjson) else 404
    return HttpResponse(status=status)


def upload_no_redirect(request):
    fs = FileSystemStorage()
    if request.method == 'POST' and request.body:
        zip = zipfile.ZipFile(io.BytesIO(request.body))
        json_name = zip.namelist()[0]
        print("JSONNAME: " + json_name)
        rl_match_id = json_name.split('.')[0]
        zip.extractall(fs.base_location)
        zip.close()

        match = RlMatch.objects.filter(rlmatchid = rl_match_id)
        if len(match) > 0 and match[0].replayjson:
            print(rl_match_id + " : file already imported")
            return

        try:
            match_data = create_match(os.path.join(fs.base_location, json_name))
            handle_match(match_data)
        except Exception as e:
            print("OS error: {0}".format(e))
            traceback.print_exc()
            return HttpResponse(status=500)

        
        return HttpResponse(status=200)

def upload_replay_no_redirect(request):
    fs = FileSystemStorage()
    
    if request.method == 'POST' and request.FILES['upfile']:
        for file in request.FILES.getlist('upfile'):

            filename = fs.save(file.name, file)
        
            if os.name == 'nt':
                print ("cmd /C C:/Users/Zoulou/Downloads/RocketLeagueReplayParser.Console.1.11.0/dist/RocketLeagueReplayParser.exe " + fs.base_location + '/'+file.name+' --fileoutput')
                p1 = subprocess.Popen(["cmd", "/C", "C:/Users/Zoulou/Downloads/RocketLeagueReplayParser.Console.1.11.0/dist/RocketLeagueReplayParser.exe " + fs.base_location + '/'+file.name+' --fileoutput'],stdout=subprocess.PIPE)
            else:
                print ("dotnet /home/ubuntu/dotnettest/RocketLeagueReplayParser.Console.Core.dll " + fs.base_location + '/'+file.name+' --fileoutput')
                p1 = subprocess.Popen(["dotnet", "/home/ubuntu/dotnettest/RocketLeagueReplayParser.Console.Core.dll " + fs.base_location + '/'+file.name+' --fileoutput'],stdout=subprocess.PIPE)
            out = p1.communicate()
            #call_command(' ', fs.base_location+'/current_replay.replay', stdout=out)
            try:
                match_data = create_match(file.name.replace('.replay', '.json'))
                os.remove(file.name.replace('.replay', '.json'))
                handle_match(match_data)
            except Exception as e:
                print("OS error: {0}".format(e))
                traceback.print_exc()

            return HttpResponse('')

def handle_match(match_data):
    
    match = RlMatch.objects.get_or_create(
        scoreblue=match_data.team_blue_score,
        scorered=match_data.team_red_score,
        starttime=match_data.date_time.strftime("%Y-%m-%d %H:%M:%S"),
        duration=match_data.duration,
        rlmatchid=match_data.id,
        replayjson=''
        )
    
    
    for player in match_data.players:
        
        player_data = match_data.players[player]
        
        user = RlUser.objects.get_or_create(onlineid=str(player_data.online_id), name=player)

        if player_data.team == 0 and match_data.team_blue_score > match_data.team_red_score:
            user[0].nbwin = user[0].nbwin + 1
        elif player_data.team == 1 and match_data.team_blue_score < match_data.team_red_score:
            user[0].nbwin = user[0].nbwin + 1
        else:
            user[0].nblose = user[0].nblose + 1

        user[0].nbmatchs = user[0].nbmatchs + 1

        user[0].nblose = user[0].nblose
        user[0].pwin = user[0].nbwin * 100 / user[0].nbmatchs
        user[0].nbgoal = user[0].nbgoal + player_data.goals
        user[0].nbassist = user[0].nbassist + player_data.assists
        user[0].nbsave = user[0].nbsave + player_data.saves
        user[0].score = user[0].score + player_data.score

        RlPlayer.objects.get_or_create(userid=user[0],
                                       idmatch=match[0],
                                       name=player_data.name,
                                       score=player_data.score,
                                       assist=player_data.assists,
                                       goal=player_data.goals,
                                       saves=player_data.saves,
                                       platform='',
                                       team=player_data.team,
                                       shot=player_data.shots)

        user[0].save()

    match[0].replayjson = json.dumps(match_data.json)
    match[0].save()