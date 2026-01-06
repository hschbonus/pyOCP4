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

    def generate_pairs():
        pass

    def create_round(self):
        if len(self.rounds) >= self.rounds_nb:
            raise ValueError("Nombre maximum de tours atteint")

        round_name = f"Round {self.current_round + 1}"
        new_round = Round(round_name)

        pairs = self.generate_pairs()

        for player1, player2 in pairs:
            new_round.create_match(player1, player2)

        self.rounds.append(new_round)
        self.current_round += 1

        return new_round
