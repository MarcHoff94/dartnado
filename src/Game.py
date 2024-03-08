from dataclasses import dataclass
import datetime
from enum import Enum



@dataclass
class Player():
    id: int
    name: str
    nickname: str
    walk_on_music: str

@dataclass
class Team():
    id: int  
    team_name: str  
    players: list[Player]


@dataclass
class Gamestatus(Enum):
    finished= "finished"
    ongoing= "ongoing"
    interrupted= "interrupted"


class Multiplier(Enum):
    SINGLE= 1
    DOUBLE= 2
    TRIPLE= 3


@dataclass
class Throw():
    """Client only handles throws and sends the result to the server"""
    multiplier: Multiplier
    value: int

@dataclass
class Round():
    round: list[Throw]
    player_id: Player.id
    number_of_throws: int


@dataclass
class Leg():
    points: dict[Team.id:int]  
    rounds: dict[Team.id:list[Round]]
    starting_team: int
    #winner: team depends if calculation is done by the server or client


@dataclass
class Set():
    legs_to_win: int    
    legs: dict[Team.id:list[Leg]]
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
    sets: dict[Team.id:list[Set]]
    current_set: Set
    game_mode: Game_Mode
    game_finished: Gamestatus
    start_time: datetime
    end_time: datetime
    standings: str = "nan"






