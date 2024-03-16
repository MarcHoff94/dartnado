from dataclasses import dataclass
from enum import Enum
from Entities.Team import Team
from pydantic import BaseModel

class GameStatus(str, Enum):
    finished= "finished"
    ongoing= "ongoing"
    interrupted= "interrupted"


class Multiplier(int, Enum):
    SINGLE= 1
    DOUBLE= 2
    TRIPLE= 3

class Throw(BaseModel):
    multiplier: Multiplier
    value: int

class GameRound(BaseModel):
    round: list[Throw]
    player_id: int

@dataclass
class Leg():
    points: dict[Team:int]  #key = team.id
    rounds: dict[Team:list[GameRound]] #key = team.id
    starting_team: int

    #winner: team depends if calculation is done by the server or client


@dataclass
class Set():
    legs_to_win: int    
    legs: dict[Team:list[Leg]] #key = team.id
    current_leg: Leg
    #won: bool
    #set_id could be added


class Check_Out(Enum):
    STRAIGHT_OUT= "STRAIGHT OUT"
    DOUBLE_OUT= "DOUBLE OUT"
    MASTER_OUT= "MASTER OUT"


class Check_In(Enum):
    STRAIGHT_IN= "STRAIGHT IN"
    DOUBLE_IN= "DOUBLE OUT"
    TRIPLE_IN= "SINGLE OUT"


@dataclass
class Game_Mode():
    sets_to_win: int
    legs_to_win_set: int
    points_per_leg: int
    check_out: Check_Out
    check_in: Check_In


#to be finished
@dataclass
class Game(): 
    game_id: int
    teams: list[Team]
    sets: dict[Team:list[Set]] #key = team.id
    current_set: Set
    game_mode: Game_Mode
    # game_finished: Gamestatus
    # start_time: datetime
    # end_time: datetime
    # standings: str = None



