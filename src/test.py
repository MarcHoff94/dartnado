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

    def create_game():
        return 




class Tournament_Tree():
    no_players: int

    def __init__(self, no_players):
        self.no_players= no_players

    @property
    def number_of_rounds(self):
        return int(round(math.log2(self.no_players),0))
    







tournament= Tournament_Tree(8)

instances = []
for rounds in range(tournament.number_of_rounds):
    print(rounds)
    no_players_per_round= 2 ** rounds
    for x in range(no_players_per_round):
        instances['Game' + str(x)] = Game()

print(instances.items())
print(tournament.number_of_rounds)







