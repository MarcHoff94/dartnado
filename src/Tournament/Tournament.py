from dataclasses import dataclass
from Entities.Team import Team
from Entities.Player import Player
from Game.Game import *
from abc import ABC, abstractmethod

from Game.Game import Game, Game_Mode

class Phase_Type(Enum):
    Single_Knockout= "Single_Knockout"
    Double_Knockout= "Double_Knockout"
    Group_Stage= "Group_Stage"

class GamePlan(ABC):
    input_teams: list[Team]
    output_teams: list[Team]
    game_mode: list[Game_Mode]

    @abstractmethod
    def get_games(self, playable:bool) -> list[Game]:
        pass

    @abstractmethod
    def register_game_result(self, finished_game: Game):
        pass

    @abstractmethod
    def determine_output_player(self):
        pass

    @abstractmethod
    def get_current_result(self) -> list[Team]:
        pass


class Group(GamePlan):
    name: str
    matches_played: dict[Team:set[Team]]
    standings: list[Team]
    placement_to_advance: int

class GroupStage(GamePlan):
    groups: list[Group]
    placement_to_advance: int

class Tournament():
    registered_teams: list[Team]
    id: int
    name: str
    phases: list[GamePlan]  
    # start_time: datetime
    # end_time: datetime
    winner: Team

    def __init__(self,registered_teams: list[Team], id:int, name: str, phases: list[GamePlan]):
        self.registered_teams= registered_teams
        self.id= id
        self.name = name
        self.phases = phases
        self.winner = None
        
