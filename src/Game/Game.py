from dataclasses import dataclass
import datetime
from enum import Enum
from Entities.Team import Team

@dataclass
class GameStatus(Enum):
    finished= "finished"
    ongoing= "ongoing"
    interrupted= "interrupted"


class Multiplier(Enum):
    SINGLE= 1
    DOUBLE= 2
    TRIPLE= 3
    def __dict__(self) -> dict:
        return {self.name: self.value}


@dataclass
class Throw():
    """Client only handles throws and sends the result to the server"""
    multiplier: Multiplier
    value: int

    def __dict__(self) -> dict:
        return {'multiplier': self.multiplier.value, 'value': self.value}

@dataclass
class Round():
    round: list[Throw]
    player_id: int
    number_of_throws: int
    def __dict__(self) -> dict:
        return {'round': [throw.__dict__() for throw in self.round], 'player_id': self.player_id, 'number_of_throws': self.number_of_throws}


@dataclass
class Leg():
    points: dict[Team:int]  #key = team.id
    rounds: dict[Team:list[Round]] #key = team.id
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
    # game_mode: Game_Mode
    # game_finished: Gamestatus
    # start_time: datetime
    # end_time: datetime
    # standings: str = "nan"


@dataclass
class Initializer():
    game: Game 
    game_mode: Game_Mode




