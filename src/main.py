from server.server import MainServer
import uvicorn
from Game.Game import Game, Set, Leg
from Entities.Player import Player
from Entities.Team import Team
from Tournament.Tournament import *

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

team_1 = Team(1, 'test1', [Player(1, 'Christoph Hermann', 'Hermanndez', 'https://www.youtube.com/watch?v=xlacPkRfVhg')])
team_2 = Team(2, 'test2', [Player(2, 'Marcus Hoffmann', 'MarcHoff94', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')])
teams = [team_1, team_2]

if __name__ == '__main__':
    app = MainServer()
    
    uvicorn.run(app, host=HOST_NAME, port=PORT_NUMBER)


    

