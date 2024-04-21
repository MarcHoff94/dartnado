from fastapi import FastAPI
from Tournament.Tournament import *
from DummyFactory.DummyFactory import generate_groupstage, generate_teams
import time


class MainServer(FastAPI):
    groupstage: GroupStage
    def __init__(self, groupstage: GroupStage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groupstage = groupstage
        # Define your endpoints here
        @self.get("/tournament/{tournament_id}/game/{game_id}")
        def get_game(tournament_id: int, game_id: int):
            time.sleep(5)
            return {"tournament_id": tournament_id, "game_id": game_id}
        
        @self.put("/tournament/{tournament_id}/game/{game_id}/round")
        def register_round(tournament_id: int, game_id: int, round: GameRound):
            return {'tournament id': tournament_id, 'game id': game_id, 'received_rounds': round.round, 'received_team_id': round.team_id}

        @self.put("/tournament/{tournament_id}/game/{game_id}/finished")
        def register_game(tournament_id: int, game_id: int, finished_game: Game):
            self.groupstage.register_game_result(finished_game)
            return {f"Game: {finished_game.teams[1].team_name} vs. {finished_game.teams[2].team_name} => Winner: {finished_game.winner}"}
        
        @self.put("/tournament/{tournament_id}/game/{game_id}/leg")
        def update_game(tournament_id: int, game_id: int, finished_leg: Leg):
            return {'tournament id': tournament_id, 'game id': game_id, 'Leg': finished_leg}
        
        @self.get("/hello")
        def greet():
            return 'Hello'