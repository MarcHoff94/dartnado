from enum import Enum
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from Entities.Team import Team
import random

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

class Check_Out(str, Enum):
    STRAIGHT_OUT= "STRAIGHT OUT"
    DOUBLE_OUT= "DOUBLE OUT"
    MASTER_OUT= "MASTER OUT"
class Check_In(str, Enum):
    STRAIGHT_IN= "STRAIGHT IN"
    DOUBLE_IN= "DOUBLE IN"
    TRIPLE_IN= "TRIPLE IN"


class GameRound(BaseModel):
    round: list[Throw]
    checked_in: bool = Field(False)
    team_id: int
    player_id: int

    def register_throw(self, new_throw:Throw, check_in_condition: Check_In) -> int | None:
        """Stores parameter new_throw and return number of throws remaining in this round"""
        if self.checked_in == False:
            if meets_check_in_condition(check_in_condition, new_throw):
                self.checked_in = True
            else:
                new_throw.value = 0
                
        self.round.append(new_throw)
        remaining_throws = 3 - len(self.round)
        if remaining_throws > 0:
            return remaining_throws
        else:
            None

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
            self.points[new_round.team_id] = result
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
    current_gameround: GameRound
    started_leg: int #team.id
    winner: Team | None = Field(None)

    # start_time: datetime
    # end_time: datetime
    # standings: str = None
    class Config:
        arbitrary_types_allowed = True
            
    def meets_check_out_condition(self, throw: Throw) -> bool:
        match self.game_mode.check_out.value:
            case 'STRAIGHT OUT':
                return True
            case 'DOUBLE OUT':
                return throw.multiplier.value == 2
            case 'MASTER OUT':
                return (throw.multiplier.value == 2) | (throw.multiplier.value == 3)


    def meets_check_in_condition(self, throw: Throw) -> bool:
        match self.game_mode.check_in.value:
            case 'STRAIGHT IN':
                self.current_gameround.checked_in = True
                return True
            case 'DOUBLE IN':
                if throw.multiplier.value == 2:
                    self.current_gameround.checked_in = True
                    return True
                else:
                    return False
            case 'TRIPLE IN':
                if throw.multiplier.value == 3:
                    self.current_gameround.checked_in = True
                    return True
                else:
                    return False
    def is_game_won(self) -> bool:
        if self.current_set.get_number_of_legs_won(self.current_gameround.team_id) == self.game_mode.legs_to_win_set:
            self.sets[self.current_gameround.team_id].append(self.current_set)

            if self.get_number_of_sets_won(self.current_gameround.team_id) == self.game_mode.sets_to_win:
                self.winner = self.teams[self.current_gameround.team_id]
                return True
            self.current_set = Set(dict.fromkeys(self.teams.keys()))

        self.current_leg = Leg(points=dict.fromkeys(self.teams.keys()), rounds=dict.fromkeys(self.teams.keys()))
        return False
       
    def register_throw(self, new_throw: Throw):

        if self.current_gameround.checked_in == False:
            if self.meets_check_in_condition(new_throw) == False:
                new_throw.value = 0

        result = self.current_leg.points[self.current_gameround.team_id] - new_throw.value
        if result < 0:
            new_throw.value = 0
            self.current_gameround.round.append(new_throw)
            while self.current_gameround.round.__len__() < 3:
                self.current_gameround.round.append(Throw(Multiplier.SINGLE, 0))   
        elif result == 0 & self.meets_check_out_condition(new_throw):
            self.current_leg.points[self.current_gameround.team_id] = result
            self.current_gameround.round.append(new_throw)
            self.current_leg.register_round(self.current_gameround)
            self.current_set.register_finished_leg(self.current_gameround.team_id, self.current_leg)
            return
        else:
            self.current_leg.points[self.current_gameround.team_id] = result


        if 3 - self.current_gameround.round.__len__() == 0:
            self.current_leg.register_round(self.current_gameround)
            #hier weiter machen, das team das nicht gespielt hat is als nächstes dran (auch noch in elif in Zeile 188 einfügen)
            next_team = 0
            self.current_gameround = GameRound(round=list(), checked_in=False, team_id=next_team, player_id=0)  
        
        
        
            
    def register_gameround(self):
        pass
    def start_game(self):
        self.started_leg = random.choice(list(self.teams.keys()))
        self.current_gameround = GameRound(round=list(), checked_in=False, team_id=self.started_leg)

    def get_number_of_sets_won(self, team_id: int) -> int:
        return len(self.sets[team_id])
    
    def finish_game(self) -> None:
        pass