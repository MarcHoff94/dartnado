from dataclasses import dataclass, field
from Entities.Player import Player

@dataclass
class Record():
    wins: int
    loses: int
    point_diff: list[int]

@dataclass
class Team():
    _id: int  
    team_name: str  
    _players: list[Player]
    wins: int = field(default=0)
    loses: int = field(default=0)
    point_diff: list[int] = field(default_factory=list)

    def __hash__(self) -> int:
        return self.id
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        raise AttributeError(f'Attribute id is immutable and cannot be modified')
    
    @property
    def players(self):
        return self._players
    @players.setter
    def players(self, value):
        if not value:
            raise ValueError("Cannot set players to an empty list")
        self._players = value
    
    def reset_stats(self):
        self.wins = 0
        self.loses = 0
        self.point_diff = list()

