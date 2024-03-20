from server.server import MainServer
import uvicorn
from Game.Game import *
from Entities.Player import Player
from Entities.Team import Team
from Tournament.Tournament import *

gamemode = Game_Mode(sets_to_win=3,legs_to_win_set=3,points_per_leg=501, check_out=Check_Out.DOUBLE_OUT, check_in=Check_In.STRAIGHT_IN)
team_1 = Team(id=1, team_name='test1', players=[Player(id=1, name='Christoph Hermann', nickname= 'Hermanndez', walk_on_music='none')])
team_2 = Team(id=2, team_name='test2', players=[Player(id=2, name='Marcus Hoffmann', nickname='MarcHoff94', walk_on_music='none')])
team_3 =Team(id=3, team_name='test3', players=[Player(id=3, name='Max Mustermann', nickname='MaxMust', walk_on_music='none')])
team_4 = Team(id=4, team_name='test4', players=[Player(id=4, name='Franz Müller', nickname='FranzyMüll', walk_on_music='none')])
teams = [team_1, team_2, team_3, team_4]

group_1 = Group(0,'test', teams, gamemode, 2)
print(len(group_1.matches))

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

if __name__ == '__main__':
    app = MainServer()
    
    uvicorn.run(app, host=HOST_NAME, port=PORT_NUMBER)


    

