import json
import copy
from player.parser.replay_data import Player, Match, Car, Team, Event, Car, Ball, Actor

from collections import defaultdict
from datetime import datetime




def create_match(filename):
    
    with open(filename) as data_file:
        data = json.load(data_file)
    
    metadata = data['Properties']
    match = get_match_data(metadata)

    add_players(match, metadata)
    add_frames(match, data['Frames'])
    
    return match
    print('end')

def get_match_data(metadata):
    
    match = Match()
    
    match.team_size = metadata['TeamSize']
    if 'Team0Score' in metadata:
        match.team_blue_score = metadata['Team0Score']
    else:
        match.team_blue_score = 0
    if 'Team1Score' in metadata:
        match.team_red_score = metadata['Team1Score']
    else:
        match.team_red_score = 0
    match.record_fps = metadata['RecordFPS']
    match.id = metadata['Id']
    match.date_time = metadata['Date'],
    match.num_frames = metadata['NumFrames']
    match.map_name = metadata['MapName']
    try:
        match.date_time = datetime.strptime(match.date_time[0], '%Y-%m-%d %H-%M-%S')
    except ValueError:
        match.date_time = datetime.strptime(match.date_time[0], '%Y-%m-%d:%H-%M')

    return match

def add_players(match, metadata):
    
    players = {}
    
    for player_data in metadata['PlayerStats']:
        player = Player()
        player.name = player_data['Name']
        player.online_id = player_data['OnlineID']
        player.team = player_data['Team']
        player.score = player_data['Score']
        player.goals = player_data['Goals']
        player.assists = player_data['Assists']
        player.saves = player_data['Saves']
        player.shots = player_data['Shots']
        players.update({player.name: player})
    
    match.players = players
    match.cars = {}
    match.ball = {}
    match.teams = {}
    match.actors = {}
    return 
        
def add_frames(match, frames_data):
    
    frames = []
    
    for frame_data in frames_data:
        
        frame = {}
        match.duration = frame_data['Time']
        frame['Time'] = frame_data['Time']
        
        
                # Check for deleted actors
        for actor_id in frame_data['DeletedActorIds']:
            if actor_id in match.ball:
                match.ball = {}
        
        for actor_update in frame_data['ActorUpdates']:
            
            if 'ClassName' not in actor_update:
                if 'TAGame.PRI_TA:MatchSaves' in actor_update:
                    get_car(match, actor_update).scoreboard['saves'] = actor_update['TAGame.PRI_TA:MatchSaves']
                if 'TAGame.PRI_TA:MatchScore' in actor_update:
                    get_car(match, actor_update).scoreboard['score'] = actor_update['TAGame.PRI_TA:MatchScore']
                if 'TAGame.PRI_TA:MatchAssists' in actor_update:
                    get_car(match, actor_update).scoreboard['assists'] = actor_update['TAGame.PRI_TA:MatchAssists']
                if 'TAGame.PRI_TA:MatchShots' in actor_update:
                    get_car(match, actor_update).scoreboard['shots'] = actor_update['TAGame.PRI_TA:MatchShots']
                if 'TAGame.PRI_TA:MatchGoals' in actor_update:
                    get_car(match, actor_update).scoreboard['goals'] = actor_update['TAGame.PRI_TA:MatchGoals']

                if 'Engine.TeamInfo:Score' in actor_update:
                    match.teams[actor_update['Id']].score = actor_update['Engine.TeamInfo:Score']
                if 'TAGame.RBActor_TA:ReplicatedRBState' in actor_update:
                    id = actor_update['Id']
                    if id in match.ball:
                        update_car_or_ball_state(match.ball[id], actor_update)
                    if id in match.cars:
                        update_car_or_ball_state(match.cars[id], actor_update)
            
            else:
                if 'TAGame.Team_Soccar_TA' == actor_update['ClassName']:
                   add_team(match, actor_update)
                
                elif 'TAGame.Car_TA' == actor_update['ClassName']:
                    if 'Engine.Pawn:PlayerReplicationInfo' in actor_update:
                        actor_id = actor_update['Engine.Pawn:PlayerReplicationInfo']['ActorId']
                        if actor_id in match.actors:
                            actor = match.actors[actor_update['Engine.Pawn:PlayerReplicationInfo']['ActorId']]
                        else:
                            actor = Actor()
                            match.actors[actor_id] = actor
                        if actor_update['Id'] in match.cars:
                            actor.car = match.cars[actor_update['Id']]
                        else:
                            match.cars[actor_update['Id']] = get_car(match, actor_update)
                            actor.car = match.cars[actor_update['Id']]
                            if actor_id in match.cars:
                                actor.car.scoreboard = match.cars[actor_id].scoreboard
                    car = get_car(match, actor_update)
                    update_car_or_ball_state(car, actor_update)
                    
                
                elif 'TAGame.Ball_TA' == actor_update['ClassName']:
                    ball_id = actor_update['Id']
                    if ball_id not in match.ball:
                         match.ball[ball_id] = Ball()
                    update_car_or_ball_state(match.ball[ball_id], actor_update)
                
                elif 'TAGame.PRI_TA' == actor_update['ClassName']:
                   
                    actor_id = actor_update['Id']
                    
                    actors = match.actors
                    
                    if actor_id not in actors:
                        actors[actor_id] = Actor()
                        actors[actor_id].car = get_car(match, actor_update)
                    if 'Engine.PlayerReplicationInfo:PlayerName' in actor_update:
                        actors[actor_id].name = actor_update['Engine.PlayerReplicationInfo:PlayerName']
                    if 'Engine.PlayerReplicationInfo:Team' in actor_update:
                        actors[actor_id].team =  actor_update['Engine.PlayerReplicationInfo:Team']['ActorId']
                    elif 'ClassName' in actor_update and actor_update['ClassName'] == 'TAGame.Team_Soccar_TA':
                        if actor_update['TypeName'] == 'Archetypes.Teams.Team0':
                            match.teams[actor_update['Id']].color = 'blue'
                        elif actor_update['TypeName'] == 'Archetypes.Teams.Team1':
                            match.teams[actor_update['Id']].color = 'red'
                        
        
        new_frame = build_frame(match)
        frames.append(new_frame)
    match.json = frames

def build_frame(match):
    
    frame = {}
    frame['time'] = match.duration
    frame['cars'] = {}
    frame['ball'] = {}
    frame['teams'] = {}

    for actor_id in match.actors:
        frame['cars'][ match.actors[actor_id].name] = copy.deepcopy(match.actors[actor_id].car).__dict__
        frame['cars'][ match.actors[actor_id].name]['name'] = match.actors[actor_id].name
        
    for id_ball in match.ball:
        frame['ball'] = copy.deepcopy(match.ball[id_ball]).__dict__
    
    for team in match.teams:
        frame['teams'][match.teams[team].color] = {'score' : match.teams[team].score}
    return frame

def update_cars(cars, actor_update):
    
    if 'TAGame.CarComponent_TA:Vehicle' not in actor_update:
        return
    
    class_name = actor_update['ClassName']
    actor_id = actor_update['TAGame.CarComponent_TA:Vehicle']['ActorId']
    
    if actor_id not in cars:
        cars.update({actor_id: get_car(match, actor_update)})
    
    car = cars[actor_id]
    
    if class_name == 'TAGame.CarComponent_Jump_TA':
        car.pos = actor_update['InitialPosition']
    
    return cars

def get_car(match, actor_update):
    id = actor_update['Id']
    if id not in match.cars:
        match.cars[id] = Car()
        match.cars[id].scoreboard = {
            'saves' : 0,
            'score' : 0,
            'assists' : 0,
            'shots' : 0,
            'goals' : 0
        }
    return match.cars[id]

def update_car_or_ball_state(car_or_ball, actor_update):
    if 'TAGame.RBActor_TA:ReplicatedRBState' in actor_update:
        state = actor_update['TAGame.RBActor_TA:ReplicatedRBState']
        if 'Position' in state:
            car_or_ball.position = state['Position']
        if 'Rotation' in state:
            car_or_ball.rotation= state['Rotation']
        if 'LinearVelocity' in state:
            car_or_ball.linear_velocity = state['LinearVelocity']
        if 'AngularVelocity' in state:
            car_or_ball.angular_velocity = state['AngularVelocity']
        if 'Sleeping' in state:
            car_or_ball.sleeping = state['Sleeping']
            
def add_team(match, actor_update):
    
    id = actor_update['Id']
    if 'Archetypes.Teams.Team0' == actor_update['TypeName']:
        match.teams[id] = Team()
        match.teams[id].color = 'blue'
        match.teams[id].score = 0
    elif 'Archetypes.Teams.Team1' == actor_update['TypeName']:
        match.teams[id] = Team()
        match.teams[id].score = 0
        match.teams[id].color = 'red'