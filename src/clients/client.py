import requests
from Game.Game import Round, Throw

throws = [Throw(multiplier=3, value=20), Throw(multiplier=3, value=20), Throw(multiplier=3, value=20)]
round_1 = Round(round=throws, player_id=1, number_of_throws=3)


url = 'http://localhost:8000'
data = round_1.__dict__
response = requests.post(url, data=data)
print("Response from server:", response.text)
