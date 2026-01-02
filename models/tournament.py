from .player import Player
from .round import Round


class Tournament:

    def __init__(self,
                 name,
                 place,
                 start_date,
                 end_date,
                 description,
                 rounds_nb=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.rounds = []
        self.rounds_nb = rounds_nb
        self.current_round = 1
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)

    def create_round(self, round: Round):
        self.rounds.append(round)
