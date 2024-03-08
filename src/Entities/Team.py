from dataclasses import dataclass
from Player import Player

@dataclass
class Team():
    id: int  
    team_name: str  
    players: list[Player]

