from server.server import MainServer
import uvicorn
from Game.Game import *
from Entities.Player import Player
from Entities.Team import Team
from Tournament.Tournament import *



HOST_NAME = 'localhost'
PORT_NUMBER = 8000

if __name__ == '__main__':
    app = MainServer()
    
    uvicorn.run(app, host=HOST_NAME, port=PORT_NUMBER)


    

