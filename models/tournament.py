class Tournoi:

    def __init__(self,
                 name,
                 place,
                 start_date,
                 end_date,
                 current_round_nb,
                 round_list, player_list,
                 description,
                 round_nb='4'):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.current_round_nb = current_round_nb
        self.rounds_list = round_list if round_list else []
        self.players_list = player_list if player_list else []
        self.description = description
        self.round_nb = round_nb
