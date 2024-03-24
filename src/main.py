from server.server import *
from fastapi import FastAPI
import uvicorn
from Tournament.Tournament import *
from DummyFactory.DummyFactory import generate_groupstage, generate_teams

registered_teams = generate_teams(1, 1, 16)
groupstage = generate_groupstage(registered_teams, 4, 1)
print(groupstage)

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

if __name__ == '__main__':
    app = MainServer(groupstage)

    uvicorn.run(app, host=HOST_NAME, port=PORT_NUMBER)


    

