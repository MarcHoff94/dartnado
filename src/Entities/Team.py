from dataclasses import dataclass
from Entities.Player import Player

@dataclass
class Team():
    id: int  
    team_name: str  
    players: list[Player]

    def __hash__(self) -> int:
        return self.id

