from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
import time
import requests
from Game.Game import *
from Entities.Player import Player

#Dummy stuff created

dartboard_values = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,50]

gamemode = Game_Mode(sets_to_win=2,legs_to_win_set=1,points_per_leg=152, check_out=Check_Out.DOUBLE_OUT, check_in=Check_In.STRAIGHT_IN)
team_1 = Team(id=1, team_name='team_1', players=[Player(id=1, name='Christoph Hermann', nickname= 'Hermanndez', walk_on_music='https://www.youtube.com/watch?v=xlacPkRfVhg')])
team_2 = Team(id=2, team_name='team_2', players=[Player(id=2, name='Marcus Hoffmann', nickname='MarcHoff94', walk_on_music='https://www.youtube.com/watch?v=dQw4w9WgXcQ')])
teams = [team_1, team_2]
game_1 = Game(
    game_id=1,
    group_name='group_1',
    teams=teams,
    game_mode=gamemode,
    sets= {team.id: [] for team in teams},
    current_set= Set(legs={team.id: list() for team in teams}),
    current_leg= Leg(points={team.id: gamemode.points_per_leg for team in teams}, rounds= {team.id: [] for team in teams}),
    )
game_1.start_game()
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
    throw_data = input_group(f'{game_1.teams[game_1.started_round].team_name} Throw {game_1.current_gameround.round.__len__()+1}/3',[
        select('points', dartboard_values, name= 'points'),
        select('multiplier', Multiplier, name= 'multiplier')
    ])
    new_throw = Throw(multiplier=throw_data['multiplier'], value=throw_data['points'])
    
    game_1.register_throw(new_throw)

    datatable_update('overview_data', [
        ['Current stats', f'{team_1.team_name} (id: {team_1.id})', f'{team_2.team_name} (id: {team_2.id})'],
        ['Sets', game_1.get_number_of_sets_won(team_id=team_1.id), game_1.get_number_of_sets_won(team_id=team_2.id)],
        ['Legs', game_1.current_set.get_number_of_legs_won(team_id=team_1.id), game_1.current_set.get_number_of_legs_won(team_id=team_2.id)],
        ['Points', game_1.current_leg.points[team_1.id], game_1.current_leg.points[team_2.id]]
    ]) 
    if game_1.winner != None:
        game_finished = True