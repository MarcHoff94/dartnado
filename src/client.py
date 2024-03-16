import requests
from dataclasses import dataclass
from Game.Game import *



throws = [Throw(multiplier=3, value=20), Throw(multiplier=3, value=20), Throw(multiplier=3, value=20)]
round = GameRound(round=throws, player_id=1)
round_dict = round.model_dump()
tournament_id = 1
game_id = 42
url = f'http://localhost:8000/tournament/{tournament_id}/game/{game_id}/round'
response = requests.put(url, json=round_dict)
print("Response from server:", response.text, response.status_code)

