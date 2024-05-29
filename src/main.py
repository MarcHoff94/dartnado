from server.server import *
from fastapi import FastAPI
import uvicorn
from Tournament.Tournament import *
from DummyFactory.DummyFactory import generate_groupstage, generate_teams, generate_games

registered_teams = generate_teams(1, 1, 16)
games = generate_games(8, 2, registered_teams, 0,Game_Mode(sets_to_win=5, legs_to_win_set=3, points_per_leg=501, check_out= Check_Out.DOUBLE_OUT, check_in= Check_In.STRAIGHT_IN))
groupstage = generate_groupstage(registered_teams, 4, 1)

x = SingleKockOut(registered_teams, Game_Mode(sets_to_win=5, legs_to_win_set=3, points_per_leg=501, check_out= Check_Out.DOUBLE_OUT, check_in= Check_In.STRAIGHT_IN), 0)
print(x)


HOST_NAME = 'localhost'
PORT_NUMBER = 8000

if __name__ == '__main__':
    app = MainServer(groupstage)

    uvicorn.run(app, host=HOST_NAME, port=PORT_NUMBER)



