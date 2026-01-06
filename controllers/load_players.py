import json

with open("../data/players.json") as file:
    players_data = json.load(file)

print(players_data)
