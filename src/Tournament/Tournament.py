from dataclasses import dataclass
from Entities.Team import Team
from Game.Game import *
from abc import ABC, abstractmethod
from itertools import combinations
import math

from Game.Game import Game, Game_Mode

class PhaseType(Enum):
    SINGLE_KNOCKOUT= "single_knockout"
    DOUBLE_KNOCKOUT= "double_knockout"
    GROUPSTAGE= "groupstage"

class GamePlan(ABC):
    input_teams: list[Team]
    output_teams: list[Team]
    game_mode: list[Game_Mode]
    phasetype: PhaseType

@dataclass
class Group():
    name: str
    matches: dict[int, Game] # key = game.game_id
    finished_matches: dict[int, Game] #key = game.game_id
    standings: list[Team]
    placement_to_advance: int

    def __init__(self,start_id: int, name: str, teams: list[Team],game_mode: Game_Mode, num_games_per_opponent: int, placement_to_advance: int) -> None:
        self.name = name
        self.standings = teams
        self.game_mode = game_mode
        self.matches = dict()
        self.finished_matches = dict()
        self.placement_to_advance = placement_to_advance
        matchups = combinations(self.standings, 2)
        for matchup in matchups:
            game = Game(
                game_id = start_id,
                group_name = name,
                teams = teams,
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

            start_id += 1

    def get_games(self) -> list[Game]:
        return list(self.matches.values())

    def register_game_result(self, finished_game: Game) -> bool:
            self.matches.pop(finished_game.game_id)
            self.finished_matches[finished_game.game_id] = finished_game
            return True

    def get_current_result(self) -> list[Team]:
         self.standings.sort(key= lambda team: (-team.wins, sum(team.point_diff)))
         return self.standings
    
    def is_group_finished(self) -> bool:
        return len(self.matches.values()) == 0
    
class GroupStage(GamePlan):
    groups: dict[str, Group] #key = Group.name
    phasetype: PhaseType = Field(PhaseType.GROUPSTAGE)

    def __init__(self, input_teams: list[Team], game_mode: list[Game_Mode]):
        self.input_teams = input_teams
        self.game_mode = game_mode
        self.groups = dict()
    def create_group(self,start_id: int, name: str, group_teams: list[Team], game_mode: Game_Mode, num_games_per_opponent: int, placement_to_advance: int):
        self.groups[name] = Group(
            start_id=start_id,
            name= name,
            teams= group_teams,
            game_mode=game_mode,
            num_games_per_opponent= num_games_per_opponent,
            placement_to_advance=placement_to_advance
            )
    def get_games_from_group(self, group_name: Group) -> list[Game]:
        self.groups[group_name].get_games()

    def register_game_result(self, finished_game: Game) -> bool:
        return self.groups[finished_game.group_name].register_game_result(finished_game)

    def get_current_result(self, group_name: str) -> list[Team]:
        return self.groups[group_name].get_current_result()
      
    def determine_output_teams(self):
        for key in self.groups:
            standings = self.groups[key].get_current_result()
            self.output_teams.extend(standings[:self.groups[key].placement_to_advance])

class KnockOutNode():
    game: Game
    game_send_to_client: bool
    def __init__(self, game: Game, previous: list) -> None:
        self.game = game
        self.game_send_to_client = False
        self.previous = previous
        self.next = None

@dataclass
class SingleKnockOut(GamePlan):
    tree: dict[int,list[KnockOutNode]]
    tree_depth: int
    def __init__(self, input_teams: list[Team], default_game_mode: Game_Mode, game_start_id: int):
        self.input_teams = input_teams
        self.phasetype = PhaseType.SINGLE_KNOCKOUT
        self.game_mode = [default_game_mode]
        total_num_teams = len(input_teams)
        self.tree_depth = self.calc_tree_depth(total_num_teams) - 1
        self.tree = self.create_empty_tree(self.tree_depth)

        for node in self.tree[self.tree_depth]:
            matchup = list()
            matchup.append(input_teams.pop(0))
            matchup.append(input_teams.pop(0))
            node.game = Game(
                game_id = game_start_id,
                group_name = "no_group",
                teams = matchup,
                game_mode= default_game_mode,
                sets= {team.id: list()  for team in matchup},
                current_set= Set(legs={team.id: list()  for team in matchup}),
                current_leg= Leg(points={team.id: default_game_mode.points_per_leg for team in matchup}, rounds= {team.id: list()  for team in matchup}),            )
            game_start_id += 1
        
        if len(input_teams) != 0:
            print(f"Could not assign all teams to tournamenttree. Following teams remain without match: {[(team.id, team.team_name) for team in input_teams]}")

        for tree_level in range(self.tree_depth-1, -1, -1):
            for node in self.tree[tree_level]:
                node.game = Game(
                    game_id= game_start_id,
                    group_name= "no_group",
                    teams= list(),
                    game_mode= default_game_mode,
                    sets= dict(),
                    current_set= Set(legs=dict()),
                    current_leg= Leg(points= dict(), rounds= dict()),
                )
                game_start_id += 1

    def calc_tree_depth(self, num_teams: int) -> int:
        return math.floor(math.log2(num_teams))
    
    def create_empty_tree(self, tree_depth: int) -> dict[int, list[KnockOutNode]]:
        tree = dict()
        for tree_level in range(tree_depth, -1, -1):
            pos_previous = 0
            num_nodes = pow(2,tree_level)
            tree[tree_level] = list()
            if tree_level == tree_depth:
                for i in range(num_nodes):
                    tree[tree_level].append(KnockOutNode(None, None))
            else:
                for i in range(num_nodes):
                    previous = list()
                    previous.append(tree[tree_level+1][pos_previous])
                    pos_previous += 1
                    previous.append(tree[tree_level+1][pos_previous])
                    pos_previous += 1
                    tree[tree_level].append(KnockOutNode(None, previous))
                    for previous_node in previous:
                        previous_node.next = tree[tree_level][-1]
        return tree

    def register_game_result(self, finished_game:Game) -> bool:
        for treelevel in self.tree:
            for node in self.tree[treelevel]:
                if node.game.game_id != finished_game.game_id:
                    continue
                node.game = finished_game
                if node.next.game != None:
                    node.next.game.add_team(finished_game.teams[finished_game.winner])
                    #node.next.game gibts noch nicht !! es müssen noch games ohne teams in init erzeugt werden 
                    return True
        return False
    
    def get_playable_games(self) -> list[Game]:
        result = list()
        for treelevel in self.tree:
            for node in self.tree[treelevel]:
                if node.game != None & node.game_send_to_client == False:
                    result.append(node.game)
        return result

@dataclass
class DoubleKnockOut(GamePlan):
    upperbracket: SingleKnockOut
    lowerbracket: dict[int, list[KnockOutNode]]
    
    def __init__(self, input_teams: list[Team], default_game_mode: Game_Mode, game_start_id: int):
        self.phasetype = PhaseType.DOUBLE_KNOCKOUT
        self.game_mode = [default_game_mode]
        self.input_teams = input_teams
        self.output_teams = list()
        self.upperbracket = SingleKnockOut(input_teams, default_game_mode, game_start_id)
        self.lowerbracket = SingleKnockOut.create_empty_tree(SingleKnockOut.calc_tree_depth(len(input_teams))-1)


    def create_lowerbracket_tree(upperbracket: SingleKnockOut) -> SingleKnockOut:
        pass

    def register_game_result(self, finished_game: Game) -> bool:

        if self.upperbracket.register_game_result(finished_game) == True:
            #HIER WEITERMACHEN Verlierer muss gespeichert werden und wenns zwei sind ein game in lowerbracket gespeichert werden
            
            return True 
        
        for treelevel in self.tree:
            for node in self.tree[treelevel]:
                if node.game.game_id == finished_game.game_id:
                    node.game = finished_game
                    return True
        return False

    def get_playable_games(self) -> list[Game]:
        result = list()
        result = self.upperbracket.get_playable_games()
        for treelevel in self.tree:
            for node in self.tree[treelevel]:
                if node.game != None & node.game_send_to_client == False:
                    result.append(node.game)
        return result
    
class Tournament():
    registered_teams: list[Team]
    start_id_games: int
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

        