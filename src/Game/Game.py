from enum import Enum
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from Entities.Team import Team
import random

class GameStatus(str, Enum):
    FINISHED= "finished"
    ONGOING= "ongoing"
    INTERRUPTED= "interrupted"
class Multiplier(int, Enum):
    SINGLE= 1
    DOUBLE= 2
    TRIPLE= 3

class Throw(BaseModel):
    multiplier: Multiplier
    value: int

class Check_Out(str, Enum):
    STRAIGHT_OUT= "straight_out"
    DOUBLE_OUT= "double_out"
    MASTER_OUT= "master_out"
class Check_In(str, Enum):
    STRAIGHT_IN= "straight_in"
    DOUBLE_IN= "double_in"
    TRIPLE_IN= "triple_in"

class GameRound(BaseModel):
    round: list[Throw]
    checked_in: bool = Field(False)
    team_id: int
    player_id: int

class Leg(BaseModel):
    points: dict[int,int]  #key = team.id
    rounds: dict[int,list[GameRound]] #key = team.id
    class Config: # as a workaround to send games as objects
        arbitrary_types_allowed = True

class Set(BaseModel): 
    legs: dict[int, list[Leg]]
    class Config:
        arbitrary_types_allowed = True

    def register_finished_leg(self,winner: int, leg: Leg):
        self.legs[winner].append(leg)

    def get_number_of_legs_won(self, team_id: int) -> int:
        return len(self.legs[team_id])


class Game_Mode(BaseModel):
    sets_to_win: int
    legs_to_win_set: int
    points_per_leg: int
    check_out: Check_Out
    check_in: Check_In

class UserInterface(ABC):
    @abstractmethod
    def register_throw(self, new_throw: Throw):
        pass
    @abstractmethod
    def finish_game(self) -> None:
        pass


class Game(BaseModel, UserInterface): 
    game_id: int
    group_name: str
    teams: list[Team] #key = team.id
    game_mode: Game_Mode
    sets: dict[int,list[Set]] #key = team.id
    current_set: Set
    current_leg: Leg
    current_gameround: GameRound | None = Field(None)
    started_round: int = Field(0) #idx of team in self.teams
    started_leg: int = Field(0) #idx of team in self.teams
    started_set: int = Field(0) #idx of team in self.teams
    winner: int | None = Field(None) #team.id

    # start_time: datetime
    # end_time: datetime
    # standings: str = None
    class Config:
        arbitrary_types_allowed = True
            
    def meets_check_out_condition(self, throw: Throw) -> bool:
        match self.game_mode.check_out.value:
            case 'straight_out':
                return True
            case 'double_out':
                return throw.multiplier.value == 2
            case 'master_out':
                return (throw.multiplier.value == 2) | (throw.multiplier.value == 3)


    def meets_check_in_condition(self, throw: Throw) -> bool:
        match self.game_mode.check_in.value:
            case 'straight_in':
                self.current_gameround.checked_in = True
                return True
            case 'double_in':
                if throw.multiplier.value == 2:
                    self.current_gameround.checked_in = True
                    return True
                else:
                    return False
            case 'triple_in':
                if throw.multiplier.value == 3:
                    self.current_gameround.checked_in = True
                    return True
                else:
                    return False
    def is_game_won(self) -> bool:
        if self.current_set.get_number_of_legs_won(self.current_gameround.team_id) == self.game_mode.legs_to_win_set:
            self.sets[self.current_gameround.team_id].append(self.current_set)

            if self.get_number_of_sets_won(self.current_gameround.team_id) == self.game_mode.sets_to_win:
                self.winner = self.teams[self.started_round]
                return True
            self.current_set = Set(legs={team.id: list() for team in self.teams})
            self.started_set = self.get_idx_next_player(self.started_set)
            self.started_leg = self.started_set
            self.started_round = self.started_set
        else:
            self.started_leg = self.get_idx_next_player(self.started_leg)
            self.started_round = self.started_leg

        self.current_gameround = GameRound(round=list(), checked_in=False, team_id=self.teams[self.started_round].id, player_id=0)
        self.current_leg = Leg(points={team.id: self.game_mode.points_per_leg for team in self.teams}, rounds={team.id: list() for team in self.teams})
        return False
       
    def register_throw(self, new_throw: Throw):

        if self.current_gameround.checked_in == False:
            if self.meets_check_in_condition(new_throw) == False:
                new_throw.value = 0

        result = self.current_leg.points[self.current_gameround.team_id] - new_throw.value*new_throw.multiplier.value
        if result < 0:
            new_throw.value = 0
            self.current_gameround.round.append(new_throw)
            while self.current_gameround.round.__len__() < 3:
                self.current_gameround.round.append(Throw(Multiplier.SINGLE, 0))   
        elif result == 0 & self.meets_check_out_condition(new_throw):
            self.current_leg.points[self.current_gameround.team_id] = result
            self.current_gameround.round.append(new_throw)
            self.current_leg.rounds[self.current_gameround.team_id].append(self.current_gameround)
            self.current_set.register_finished_leg(self.current_gameround.team_id, self.current_leg)
            if self.is_game_won():
                return
        else:
            self.current_leg.points[self.current_gameround.team_id] = result
            self.current_gameround.round.append(new_throw)


        if 3 - self.current_gameround.round.__len__() == 0:
            self.current_leg.rounds[self.current_gameround.team_id].append(self.current_gameround)
            self.started_round = self.get_idx_next_player(self.started_round)    
            self.current_gameround = GameRound(round=list(), checked_in=False, team_id=self.teams[self.started_round].id, player_id=0)  

    def get_idx_next_player(self, started_idx: int) -> int:
        if started_idx == self.teams.__len__()-1:
            started_idx = 0
        else:
            started_idx += 1  
        return started_idx  

    def start_game(self):
        self.started_round = random.choice(range(0,self.teams.__len__()))
        self.started_leg = self.started_round
        self.started_set = self.started_round
        self.current_gameround = GameRound(round=list(), checked_in=False, team_id=self.teams[self.started_round].id, player_id= 0)

    def get_number_of_sets_won(self, team_id: int) -> int:
        return len(self.sets[team_id])
    
    def finish_game(self) -> None:
        pass