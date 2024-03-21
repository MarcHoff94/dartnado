from dataclasses import dataclass
import numpy as np
import math

@dataclass
class Player():
    """Class that represents players"""
    player_name: str
    id: int


class Game () :
    player1: int
    player2: int
    winner: None

    def __init__(self,team1,team2) -> None:
        self.team1= team1
        self.team2= team2
    
    def __str__(self) -> str:
        return f"Team 1: {self.team1}, Team 2: {self.team2}"


    def create_game():
        return 




class Tournament_Tree():
    no_players: int

    def __init__(self, no_players):
        self.no_players= no_players

    @property
    def number_of_rounds(self):
        return int(round(math.log2(self.no_players),0))
    

teamlist= [1,2,3,4]

tournament= Tournament_Tree(8)

instances = {}
# for rounds in range(tournament.number_of_rounds,1,-1):
#     print(rounds)
no_teams_per_round= 8#2 ** rounds
for x,z in enumerate(range( no_teams_per_round,int(no_teams_per_round/2),-1)): 
    game_id= 'Game'+ str(x)
    instances[game_id] = Game(team1=x+1,team2=z)

for instance in instances:
    print(instances[instance])



# import math

# def tournament_round( no_of_teams , matchlist ):
#     new_matches = []
#     for team_or_match in matchlist:
#         if type(team_or_match) == type([]):
#             new_matches += [ tournament_round( no_of_teams, team_or_match ) ]
#         else:
#             new_matches += [ [ team_or_match, no_of_teams + 1 - team_or_match ] ]
#     return new_matches

# def flatten_list( matches ):
#     teamlist = []
#     for team_or_match in matches:
#         if type(team_or_match) == type([]):
#             teamlist += flatten_list( team_or_match )
#         else:
#             teamlist += [team_or_match]
#     return teamlist

# def generate_tournament( num ):
#     num_rounds = math.log( num, 2 )
#     if num_rounds != math.trunc( num_rounds ):
#         raise ValueError( "Number of teams must be a power of 2" )
#     teams = 1
#     result = [1]
#     while teams != num:
#         teams *= 2
#         result = tournament_round( teams, result )
#     return result
#     #return flatten_list( result )


# tournament= generate_tournament(32)
# print(tournament)

