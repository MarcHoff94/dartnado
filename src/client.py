import requests
import json
from Game.Game import Throw, Round

throws = [Throw(multiplier=3, value=20), Throw(multiplier=3, value=20), Throw(multiplier=3, value=20)]


url = 'http://localhost:8000'
for throw in throws:
    json_data = json.dumps(throw.__dict__())
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data= json_data, headers= headers)
    print("Response from server:", response.text)
