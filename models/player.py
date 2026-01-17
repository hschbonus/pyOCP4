import json


class Player:

    def __init__(self, lastname, firstname, birth_date, national_id):
        self.lastname = lastname
        self.firstname = firstname
        self.birth_date = birth_date
        self.national_id = national_id

    def __str__(self):
        return (f"{self.lastname} {self.firstname}, "
                f"né(e) le {self.birth_date}, ID: {self.national_id}")

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"

    def to_dict(self):
        player_dict = {
            'lastname': self.lastname,
            'firstname': self.firstname,
            'birth_date': self.birth_date,
            'national_id': self.national_id,
        }
        return player_dict

    # @staticmethod
    # def load_from_json():
    #     with open('data/db.json', 'r', encoding='utf-8') as file:
    #         data = json.load(file)
    #     return data

    # def save_in_json(self):
    #     players_data = []
    #     try:
    #         players_data.extend(Player.load_from_json())
    #     except json.decoder.JSONDecodeError:
    #         pass
    #     players_data.append(self.to_dict())
    #     with open('data/db.json', 'w', encoding='utf-8') as file:
    #         json.dump(players_data, file, indent=4, ensure_ascii=False)
