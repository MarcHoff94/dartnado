from dataclasses import dataclass
from enum import Enum

@dataclass
class Game():
    player1: str
    player2: str

test = Game(player1="test1", player2="test2")
print(test.__dict__)

class Game_status(Enum):
    FINISHED = 'finished'
    ONGOING =  'ongoing'

test2 = Game_status.ONGOING
match test2:
    case Game_status.FINISHED:
        print(test2)
    case Game_status.ONGOING:
        print(test2)