from dataclasses import dataclass, field
from Entities.Team import Team
from Entities.Player import Player
from Game.Game import *
from abc import ABC, abstractmethod
from itertools import combinations

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
    def get_games(self) -> list[Game]:
        pass

    @abstractmethod
    def register_game_result(self, finished_game: Game):
        pass

    @abstractmethod
    def determine_output_player(self, placement_to_advance: int) -> list[Team]:
        pass

    @abstractmethod
    def get_current_result(self) -> list[Team]:
        pass
@dataclass
class Group():
    name: str
    matches: dict[int, Game] # key = game.game_id
    finished_matches: dict[int, Game] #key = game.game_id
    standings: list[Team]

    def __init__(self,start_id: int, name: str, teams: list[Team],game_mode: Game_Mode, num_games_per_opponent: int) -> None:
        self.name = name
        self.standings = teams
        self.game_mode = game_mode
        self.matches = dict()
        self.finished_matches = dict()
        start_id = 0
        matchups = combinations(self.standings, 2)
        for matchup in matchups:
            start_id += 1
            game = Game(
                game_id = start_id, 
                group_name= self.name,
                teams = matchup,
                game_mode= self.game_mode,
                sets= {team.id: list()  for team in matchup},
                current_set= Set(legs={team.id: list()  for team in matchup}),
                current_leg= Leg(points={team.id: game_mode.points_per_leg for team in matchup}, rounds= {team.id: list()  for team in matchup}),
                starts_leg= matchup[0].id
            )
            self.matches[game.game_id] = game
            for i in range(num_games_per_opponent-1):
                additonal_game = game
                start_id += 1
                additonal_game.game_id = start_id
                self.matches[additonal_game.game_id] = additonal_game

    def get_games(self) -> list[Game]:
        return self.matches.values()

    def register_game_result(self, finished_game: Game):
            self.matches.pop(finished_game.game_id)
            self.finished_matches[finished_game.game_id] = finished_game

    def get_current_result(self) -> list[Team]:
         return self.standings.sort(key= lambda team: (-team.wins, sum(team.point_diff)))
    
    def is_group_finished(self) -> bool:
        return len(self.matches.values()) == 0
class GroupStage(GamePlan):
    groups: dict[str, Group] #key = Group.name
    placement_to_advance: int

    def get_games(self) -> list[Game]:
        return super().get_games()
    def register_game_result(self, finished_game: Game):
        return super().register_game_result(finished_game)
    def get_current_result(self) -> list[Team]:
        return super().get_current_result()
    def determine_output_player(self, placement_to_advance: int) -> list[Team]:
        return super().determine_output_player(placement_to_advance)    
    
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
        
