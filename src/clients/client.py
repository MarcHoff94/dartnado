import requests
from dataclasses import dataclass
from enum import Enum



class Game_status(Enum):
    FINISHED = 'finished'
    ONGOING =  'ongoing'


@dataclass
class Game():
    playerx: str
    playery: str
    status: Game_status
    def __init__(self, player1: str, player2: str, status: Game_status):
        self.playerx = player1
        self.playery = player2
        self.status = status

url = 'http://localhost:8000'
data = {'key': '180!!!'}  
response = requests.get(url)
print("Response from server:", response.text)
