from dataclasses import dataclass
from Entities.Team import Team
from Entities.Player import Player
from Game.Game import *







class Phase_Type(Enum):
    Single_Knockout= "Single_Knockout"
    Double_Knockout= "Double_Knockout"
    Group_Stage= "Group_Stage"


class Game_Plan():
    


@dataclass
class Phase():
    
    input_player: list[Team]
    output_player: list[Team]
    type: Phase_Type

    def create_game_plan(self):
        match self.type.value: 
            case "Single_Knockout":
                self.create_single_knockout()
            case "Double_Knockout":
                self.create_double_knockout()
            case "Group_Stage":
                self.create_group_stage()

                
    def create_single_knockout(self):
        pass

    def create_double_knockout(self):
        pass

    def create_group_stage():
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
        
