from dataclasses import dataclass
from Entities.Team import Team
from Entities.Player import Player
from Game.Game import *
from abc import ABC, abstractmethod
from typing import Protocol

class Phase_Type(Enum):
    Single_Knockout= "Single_Knockout"
    Double_Knockout= "Double_Knockout"
    Group_Stage= "Group_Stage"

class GamePlan(Protocol):
    def get_next_game(team: Team) -> Game:
        pass

    def is_PhaseRound_finished() -> bool:
        pass
    


@dataclass
class Phase(ABC):
    
    input_player: list[Team]
    output_player: list[Team]
    type: Phase_Type
    game_plan: GamePlan

    @abstractmethod
    def create_game_plan(self):
        pass
    


class Tournament():
    registered_teams: list[Team]
    id: int
    name: str
    phases: list[Phase]  
    # start_time: datetime
    # end_time: datetime
    winner: Team

    def __init__(self,registered_teams,id,name,phases):
        self.registered_teams= registered_teams
        self.id= id
        self.name = name
        self.phases = phases
        self.winner = None
        
