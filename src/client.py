import requests
import json
from dataclasses import dataclass
from enum import Enum
from Game.Game import Throw, Multiplier

class ClientMessageType(Enum):
    THROW = 'Throw'

    def __dict__(self) -> dict:
        return {self.name: self.value}

@dataclass
class ClientMessage():
    type: ClientMessageType
    data: dict
    
    def __dict__(self) -> dict:
        return {'type': self.type.value, 'data': self.data}

throws = [Throw(multiplier=Multiplier.TRIPLE, value=20), Throw(multiplier=Multiplier.TRIPLE, value=20), Throw(multiplier=Multiplier.TRIPLE, value=20)]

url = 'http://localhost:8000'
for throw in throws:
    msg = ClientMessage(ClientMessageType.THROW, throw.__dict__())
    json_data = json.dumps(msg.__dict__())
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data= json_data, headers= headers)
    print("Response from server:", response.text)

