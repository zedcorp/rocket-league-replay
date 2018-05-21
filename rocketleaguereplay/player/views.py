import copy
import json
import os
import zipfile
import traceback
import io
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from player.conf import PlayerConf
from player.models import RlMatch, RlPlayer, RlUser
from player.parser.data.data_loader import load_data
from player.parser.data.object_numbers import get_player_info
from player.parser.parser.frames import get_frames, get_stats

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
      matchs = RlMatch.objects.filter(id = userPlayer.idmatch_id)
      for match in matchs:
        nameBlue = []
        nameRed = []
        for matchPlayer in RlPlayer.objects.filter(idmatch = match):
          if matchPlayer.team == 0:
            nameBlue.append(matchPlayer.name)
          if matchPlayer.team == 1:
            nameRed.append(matchPlayer.name)
        
        win = (userPlayer.team == 0 and match.scoreblue > match.scorered) or (userPlayer.team == 1 and match.scoreblue < match.scorered)
        
        data.append({
          'datetime': match.starttime.strftime("%d/%m/%y %H:%M"),
          'name1': nameBlue,
          'name2': nameRed,
          'score1': match.scoreblue,
          'score2': match.scorered,
          'win' : win,
          'rlmatchid': match.rlmatchid
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
            load_data(os.path.join(fs.base_location, json_name))
        except Exception as e:
            print("OS error: {0}".format(e))
            traceback.print_exc()

        handle_json(fs, rl_match_id)

        return HttpResponse('')


def handle_json(fs, rl_match_id):
    ################# dirty part should change the load_data instead #################
    frames = get_frames()
    player_info = get_player_info()
    step = 1
    myframes = [len(frames) / step]
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
        scoreblue=stats['blueteamscore'],
        scorered=stats['redteamscore'],
        starttime=stats['starttime'],
        duration=stats['duration'],
        rlmatchid=stats['matchid'])
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
                                       idmatch=match[0],
                                       name=player['Name'],
                                       score=player['Score'],
                                       assist=player['Assists'],
                                       goal=player['Goals'],
                                       saves=player['Saves'],
                                       platform=player['Platform']['Value'],
                                       team=player['Team'],
                                       shot=player['Shots'])

        user[0].save()
    for i in range(0, len(frames), step):
        if (i > 0):
            myframes.append(copy.deepcopy(myframes[int(i / step - 1)]))

        myframes[int(i / step - 1)]['time'] = frames[i]['time']['real_replay_time']
        myframes[int(i / step - 1)]['scoreboard'] = frames[i]['scoreboard']
        myframes[int(i / step - 1)]['cars'] = frames[i]['cars']
        myframes[int(i / step - 1)]['ball'] = frames[i]['ball']

        for car in myframes[int(i / step - 1)]['cars']:
            myframes[int(i / step - 1)]['cars'][car]['name'] = player_info[car]['name']
    print("FINAL: " + os.path.join(fs.base_location, rl_match_id) + '.final.json')
    filefinal = open(os.path.join(fs.base_location, rl_match_id) + '.final.json', 'w')
    encoded_str = json.dumps(myframes)
    filefinal.write(encoded_str)
    match[0].replayjson = encoded_str
    match[0].save()