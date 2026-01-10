# from rich import print
from models.player import Player
# import json

hervé = Player('schmidt', 'hervé', 'date', 'id')
# print(hervé.to_dict())
hervé.save_in_json()




 
