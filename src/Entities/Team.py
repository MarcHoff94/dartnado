from pydantic import BaseModel, Field
from Entities.Player import Player

class Team(BaseModel):
    id: int  
    team_name: str  
    players: list[Player]
    wins: int = Field(default=0)
    loses: int = Field(default=0)
    point_diff: list[int] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self) -> int:
        return self.id
    
    def reset_stats(self):
        self.wins = 0
        self.loses = 0
        self.point_diff = list()

