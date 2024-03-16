import requests
tournament_id = 1
game_id = 42
# Make a GET request to the FastAPI server
response = requests.get(f"http://localhost:8000/tournament/game?tournament_id={tournament_id}&game_id={game_id}")

# Print the response
print(response.json())
