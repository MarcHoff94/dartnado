
import time
from http.server import HTTPServer
from server.server import MainServer
from Game.Game import Game, Set, Leg
from Entities.Player import Player
from Entities.Team import Team


HOST_NAME = 'localhost'
PORT_NUMBER = 8000

team_1 = Team(1, 'test1', [Player(1, 'Christoph Hermann', 'Hermanndez', 'https://www.youtube.com/watch?v=xlacPkRfVhg')])
team_2 = Team(2, 'test2', [Player(2, 'Marcus Hoffmann', 'MarcHoff94', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')])
teams = [team_1, team_2]
game_1 = Game(1, teams, dict.fromkeys(teams), Set(5, dict.fromkeys(teams), Leg(501, dict.fromkeys, 1)) )

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MainServer)
    
    print(time.asctime(), f"Server running on : {HOST_NAME}, Port: {PORT_NUMBER}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print(time.asctime(), f"Server going down: {HOST_NAME}, Port: {PORT_NUMBER}")


class Group():
    matches_played: dict[Team:set[Team]]
    standings: dict[Team:]
    

