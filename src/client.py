import requests
from Game.Game import *
from Entities.Player import Player

gamemode = Game_Mode(sets_to_win=3,legs_to_win_set=3,points_per_leg=501, check_out=Check_Out.DOUBLE_OUT, check_in=Check_In.STRAIGHT_IN)
team_1 = Team(id=1, team_name='test1', players=[Player(id=1, name='Christoph Hermann', nickname= 'Hermanndez', walk_on_music='https://www.youtube.com/watch?v=xlacPkRfVhg')])
team_2 = Team(id=2, team_name='test2', players=[Player(id=2, name='Marcus Hoffmann', nickname='MarcHoff94', walk_on_music='https://www.youtube.com/watch?v=dQw4w9WgXcQ')])
teams = [team_1, team_2]
game_1 = Game(
    game_id=1,
    teams=teams,
    game_mode=gamemode,
    sets= {team.id: list()  for team in teams},
    current_set= Set(legs={team.id: list()  for team in teams}),
    current_leg= Leg(points={team.id: gamemode.points_per_leg for team in teams}, rounds= {team.id: list()  for team in teams}),
    starts_leg= team_1.id
    )
tournament_id = 1

game_dict = game_1.model_dump()
url = f'http://localhost:8000/tournament/{tournament_id}/game/{game_1.game_id}/finished'
response = requests.put(url, json=game_dict)
print("Response from server:", response.text, response.status_code)

