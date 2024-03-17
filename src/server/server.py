from fastapi import FastAPI
from Game.Game import *

class MainServer(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define your endpoints here
        @self.get("/tournament/{tournament_id}/game/{game_id}")
        def get_game(tournament_id: int, game_id: int):
            return {"tournament_id": tournament_id, "game_id": game_id}
        
        @self.put("/tournament/{tournament_id}/game/{game_id}/round")
        def register_round(tournament_id: int, game_id: int, round: GameRound):
            
            return {'tournament id': tournament_id, 'game id': game_id, 'received_rounds': round.round, 'received_team_id': round.team_id}

        @self.put("/tournament/{tournament_id}/game/{game_id}/finished")
        def register_game(tournament_id: int, game_id: int, finished_game: Game):
            return {'tournament id': tournament_id, 'game id': game_id, 'received_game': finished_game}