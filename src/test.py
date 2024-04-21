from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
import time
import requests
from Game.Game import *
from Entities.Player import Player
#Dummy stuff created
dartboard_values = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]

gamemode = Game_Mode(sets_to_win=3,legs_to_win_set=3,points_per_leg=501, check_out=Check_Out.DOUBLE_OUT, check_in=Check_In.DOUBLE_IN)
team_1 = Team(id=1, team_name='team_1', players=[Player(id=1, name='Christoph Hermann', nickname= 'Hermanndez', walk_on_music='https://www.youtube.com/watch?v=xlacPkRfVhg')])
team_2 = Team(id=2, team_name='team_2', players=[Player(id=2, name='Marcus Hoffmann', nickname='MarcHoff94', walk_on_music='https://www.youtube.com/watch?v=dQw4w9WgXcQ')])
teams = {team_1.id: team_1, team_2.id: team_2}
game_1 = Game(
    game_id=1,
    group_name='group_1',
    teams=teams,
    game_mode=gamemode,
    sets= {team_id: [] for team_id in teams},
    current_set= Set(legs={team_id: [] for team_id in teams}),
    current_leg= Leg(points={team_id: gamemode.points_per_leg for team_id in teams}, rounds= {team_id: [] for team_id in teams}),
    starts_leg= team_1.id
    )
tournament_id = 1

#Building interactive UI
put_text('Getting game from tournament server...')
with put_loading():
    
    url = f'http://localhost:8000/tournament/{tournament_id}/game/{game_1.game_id}'
    response = requests.get(url)
    if response.status_code != 200:
        put_text(f'Warning! could not receive game from server. Status code from response: {response.status_code}')
        time.sleep(10)
        exit()

    put_text('successfully received playable game')
    time.sleep(5)

clear()

put_datatable([
    ['Current stats', f'{team_1.team_name} (id: {team_1.id})', f'{team_2.team_name} (id: {team_2.id})'],
    ['Sets', game_1.get_number_of_sets_won(team_id=team_1.id), game_1.get_number_of_sets_won(team_id=team_2.id)],
    ['Legs', game_1.current_set.get_number_of_legs_won(team_id=team_1.id), game_1.current_set.get_number_of_legs_won(team_id=team_2.id)],
    ['Points', game_1.current_leg.points[team_1.id], game_1.current_leg.points[team_2.id]]
], instance_id='overview_data') 


game_finished = False
while game_finished == False:
    current_team_id = team_2.id
    last_round_played = GameRound(round=list(), team_id=current_team_id, player_id=0)
    round_finished = False
    nth_throw = 0
    while round_finished == False:
        nth_throw += 1
        throw_data = input_group(f'Throw {nth_throw}/3',[
            select('points', dartboard_values, name= 'points'),
            select('multiplier', Multiplier, name= 'multiplier')
        ])
        new_throw = Throw(multiplier=throw_data['multiplier'], value=throw_data['points'])
        
        if last_round_played.register_throw(new_throw, game_1.game_mode.check_in) == None:
            round_finished = True
            nth_throw = 0

    if game_1.register_round(last_round_played) == None:
            game_finished = True

    datatable_update('overview_data', [
        ['Current stats', f'{team_1.team_name} (id: {team_1.id})', f'{team_2.team_name} (id: {team_2.id})'],
        ['Sets', game_1.get_number_of_sets_won(team_id=team_1.id), game_1.get_number_of_sets_won(team_id=team_2.id)],
        ['Legs', game_1.current_set.get_number_of_legs_won(team_id=team_1.id), game_1.current_set.get_number_of_legs_won(team_id=team_2.id)],
        ['Points', game_1.current_leg.points[team_1.id], game_1.current_leg.points[team_2.id]]
    ]) 