from models.player import Player

hervé = Player('schmidt', 'hervé', 'date', 'id')
# print(hervé.to_dict())
hervé.save_in_json()
