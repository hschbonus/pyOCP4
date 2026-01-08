from .player import Player
from .round import Round
from .match import Match


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
        """Ajoute player au tournoi"""
        self.players.append(player)

    def generate_pairs(self):
        """Génère les paires servant à la constitution des matchs en fonction du round en cours"""
        pairs = []

        if self.current_round == 0:
            players_copy = self.players.copy()
            random.shuffle(players_copy)
            for i in range(0, len(players_copy), 2):
                pairs.append((players_copy[i], players_copy[i + 1]))

        else :
            players_with_score = []
            for player in self.players:
                player_score = self.get_player_score(player)
                players_with_score.append((player, player_score))
            players_with_score.sort(key=lambda x: x[1], reverse=True)
            players_available_for_pairing = []
            for player in players_with_score:
                players_available_for_pairing.append(player[0])
            c = 0
            while len(players_available_for_pairing) > 2:
                pairing_result = self.has_played_together(players_available_for_pairing[0], players_available_for_pairing[1+c])
                if pairing_result :
                    c += 1
                else:
                    pairs.append((players_available_for_pairing[0], players_available_for_pairing[1+c]))
                    players_available_for_pairing.pop(0)
                    players_available_for_pairing.pop(1+c)
                    c = 0
            pairs.append((players_available_for_pairing[0], players_available_for_pairing[1]))
        return pairs

    def create_round(self):
        if len(self.rounds) >= self.rounds_nb:
            raise ValueError("Nombre maximum de tours atteint")

        round_name = f"{self.name} - Round {self.current_round + 1}"
        new_round = Round(round_name)

        pairs = self.generate_pairs()

        for player1, player2 in pairs:
            new_round.create_match(player1, player2)

        self.rounds.append(new_round)
        self.current_round += 1

        return new_round

    def has_played_together(self, player1, player2):
        """Vérifie si deux joueurs ont déjà joué ensemble"""

        for round in self.rounds:
            for match in round.match_list:
                if player1 in [match.player1, match.player2] and player2 in [match.player1, match.player2]:
                    return True
        return False
    
    def get_player_score(self, player):
        """Calcule le score total d'un joueur dans le tournoi"""
        total_score = 0
        
        for round in self.rounds:
            for match in round.match_list:
                if player == match.player1 :
                    total_score += match.player1_score
                elif player == match.player2 :
                    total_score += match.player2_score

        return total_score

