from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from Entities.Team import Team


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
    team_id: int
    player_id: int


class Leg(BaseModel):
    points: dict[int,int]  #key = team.id
    rounds: dict[int,list[GameRound]] #key = team.id
    class Config: # as a workaround to send games as objects
        arbitrary_types_allowed = True

    #winner: team depends if calculation is done by the server or client
    def register_round(self, new_round: GameRound) -> int:
        """updates Leg.points for new_round.team_id and returns the remaining points for this team. 
        If None is returned the team overthrew and the point total is not changed"""
        self.rounds[new_round.team_id].append(new_round)
        result = self.points[new_round.team_id] - sum([throw.value*throw.multiplier for throw in new_round.round])

        if result >= 0:
            self.points = result
            return result
        else:
            return self.points
        


class Set(BaseModel): 
    legs: dict[int, list[Leg]]
    class Config:
        arbitrary_types_allowed = True

    def register_finished_leg(self,winner: int, leg: Leg):
        self.legs[winner].append(leg)

    def get_number_of_legs_won(self, team_id: int) -> int:
        return len(self.legs[team_id])


class Check_Out(str, Enum):
    STRAIGHT_OUT= "STRAIGHT OUT"
    DOUBLE_OUT= "DOUBLE OUT"
    MASTER_OUT= "MASTER OUT"


class Check_In(str, Enum):
    STRAIGHT_IN= "STRAIGHT IN"
    DOUBLE_IN= "DOUBLE OUT"
    TRIPLE_IN= "SINGLE OUT"


class Game_Mode(BaseModel):
    sets_to_win: int
    legs_to_win_set: int
    points_per_leg: int
    check_out: Check_Out
    check_in: Check_In

class UserInterface(ABC):
    @abstractmethod
    def register_round(self, new_round: GameRound) -> Leg | None:
        pass
    @abstractmethod
    def finish_game(self) -> None:
        pass


class Game(BaseModel, UserInterface): 
    game_id: int
    group_name: str
    teams: dict[int,Team] #key = team.id
    game_mode: Game_Mode
    sets: dict[int,list[Set]] #key = team.id
    current_set: Set
    current_leg: Leg
    starts_leg: int #team.id
    winner: Team | None = Field(None)

    # start_time: datetime
    # end_time: datetime
    # standings: str = None
    class Config:
        arbitrary_types_allowed = True
    
    def register_round(self, new_round: GameRound) -> Leg | None:
        """registers round in game and returns the next leg that is gonna be played. If the game is over, None is returned"""
        result = self.current_leg.register_round(new_round)
        if result == 0:
            self.current_set.register_finished_leg(new_round.team_id, self.current_leg)

            if self.current_set.get_number_of_legs_won(new_round.team_id) == self.game_mode.legs_to_win_set:
                self.sets[new_round.team_id].append(self.current_set)

                if self.get_number_of_sets_won(new_round.team_id) == self.game_mode.sets_to_win:
                    self.winner = self.teams[new_round.team_id]
                    return None
                self.current_set = Set(dict.fromkeys(self.teams.keys()))

            self.current_leg = Leg(points=dict.fromkeys(self.teams.keys()), rounds=dict.fromkeys(self.teams.keys()))
            return self.current_leg
        return None
    
    def get_number_of_sets_won(self, team_id: int) -> int:
        return len(self.sets[team_id])
    
    def finish_game(self) -> None:
        pass