import json
from django.http import HttpResponse
from django.shortcuts import render
from player.conf import PlayerConf
from player.models import RlMatch, RlPlayer, RlUser

settings = PlayerConf()

def list():
    return render(request, 'player/playerlist.html')

def test(request):
    return HttpResponse('BLABLABLA')

def list_players(request):
    players = RlUser.objects.all().order_by('-nbmatchs')

    data = []

    for player in players:
        data.append({
            'id': player.id,
            'name': player.name,
            'nbmatchs': player.nbmatchs,
            'nbwin': player.nbwin,
            'nblose': player.nblose,
            'pwin': player.pwin,
            'pscore': player.score / player.nbmatchs,
            'nbgoalpermatch': player.nbgoal / player.nbmatchs,
            'nbassistpermatch': player.nbassist / player.nbmatchs,
            'nbsavepermatch': player.nbsave / player.nbmatchs,
            'score': player.score,
            'nbgoal': player.nbgoal,
            'nbassist': player.nbassist,
            'nbsave': player.nbsave
        })
    return HttpResponse(json.dumps(data))


def player(request, id):
    players = RlUser.objects.filter(id=id)
    if len(players) > 0:
        player = players[0]
        response = {
            'id': player.id,
            'name': player.name,
            'nbmatchs': player.nbmatchs,
            'nbwin': player.nbwin,
            'nblose': player.nblose,
            'pwin': player.pwin,
            'pscore': player.score / player.nbmatchs,
            'nbgoalpermatch': player.nbgoal / player.nbmatchs,
            'nbassistpermatch': player.nbassist / player.nbmatchs,
            'nbsavepermatch': player.nbsave / player.nbmatchs,
            'score': player.score,
            'nbgoal': player.nbgoal,
            'nbassist': player.nbassist,
            'nbsave': player.nbsave
        }
        return HttpResponse(json.dumps(response))
    else:
        return HttpResponse(status=404)


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
                'datetime': match.starttime.timestamp(),
                'name1': nameBlue,
                'name2': nameRed,
                'score1': match.scoreblue,
                'score2': match.scorered,
                'win' : win,
                'rlmatchid': match.rlmatchid
            })


    jsonData = json.dumps(data)
    # jsonData = json_serialized_objects = serializers.serialize("json", users)
    return HttpResponse(jsonData)


def replay(request, match_id):
    print("REPLAY: " + match_id)
    match = RlMatch.objects.filter(rlmatchid = match_id)
    print("SIZE: " + str(len(match[0].replayjson)))
    response = HttpResponse(content=match[0].replayjson)
    return response


def replays(request):
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
    return HttpResponse(json.dumps(data))