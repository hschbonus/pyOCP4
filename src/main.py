class Joueur:

    def __init__(self, family_name, first_name, birth_date, national_id):
        family_name = self.family_name
        first_name = self.first_name
        birth_date = self.birth_date
        national_id = self.national_id


class Tournament:

    def __init__(self,
                 name,
                 place,
                 start_date,
                 end_date,
                 current_round_nb,
                 rounds_list, players_list,
                 description,
                 round_nb='4'):
        name = self.name
        place = self.place
        start_date = self.start_date
        end_date = self.end_date
        current_round_nb = self.current_round_nb
        rounds_list = []
        players_list = []
        description = self.description
        round_nb = self.round_nb
