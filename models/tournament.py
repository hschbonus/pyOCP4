import random
from datetime import datetime
from .player import Player
from .round import Round
# from .match import Match


class Tournament:

    def __init__(self,
                 name,
                 place,
                 description,
                 rounds_nb=4):
        self.name = name
        self.place = place
        self.start_date = datetime.now()
        self.end_date = None
        self.description = description
        self.rounds = []
        self.rounds_nb = rounds_nb
        self.current_round = 1
        self.players = []

    def __repr__(self):
        return (f"Tournament(name='{self.name}', place='{self.place}', "
                f"start_date='{self.start_date}', end_date='{self.end_date}', "
                f"rounds_nb={self.rounds_nb}, current_round={self.current_round}, "
                f"players={len(self.players)})")

    def add_player(self, player: Player):
        """
        Ajoute un joueur à la liste des participants du tournoi.

        Args:
        player (Player): Instance de Player à ajouter au tournoi
        """
        self.players.append(player)

    def generate_pairs(self):
        """
        Génère les paires de joueurs pour le round en cours.

        Pour le premier round (current_round == 0): mélange aléatoire des joueurs.
        Pour les rounds suivants: tri par score décroissant, appariement en évitant
        les matchs déjà joués.

        Returns:
            list: Liste de tuples (player1, player2) représentant les paires de joueurs
        """

        pairs = []

        if self.current_round == 0:
            players_copy = self.players.copy()
            random.shuffle(players_copy)
            for i in range(0, len(players_copy), 2):
                pairs.append((players_copy[i], players_copy[i + 1]))

        else:
            players_with_score = []
            for player in self.players:
                player_score = self.get_player_score(player)
                players_with_score.append((player, player_score))
            players_with_score.sort(key=lambda x: x[1], reverse=True)
            players_available_for_pairing = []
            for player in players_with_score:
                players_available_for_pairing.append(player[0])
            c = 0
            while len(players_available_for_pairing) >= 2 and 1 + c < len(players_available_for_pairing):
                pairing_result = self.has_played_together(
                    players_available_for_pairing[0],
                    players_available_for_pairing[1 + c]
                )
                if pairing_result:
                    c += 1
                else:
                    pairs.append((players_available_for_pairing[0], players_available_for_pairing[1 + c]))
                    players_available_for_pairing.pop(1 + c)
                    players_available_for_pairing.pop(0)
                    c = 0

            while len(players_available_for_pairing) >= 2:
                pairs.append((players_available_for_pairing[0], players_available_for_pairing[1]))
                players_available_for_pairing.pop(1)
                players_available_for_pairing.pop(0)
        return pairs

    def create_round(self):
        """
        Crée un nouveau round avec génération automatique des paires et des matchs.

        Génère les paires via generate_pairs(), crée les matchs correspondants,
        ajoute le round à la liste des rounds et incrémente current_round.

        Returns:
            Round: L'instance du round créé

        Raises:
            ValueError: Si le nombre maximum de rounds (rounds_nb) est atteint
        """

        if len(self.rounds) >= self.rounds_nb:
            raise ValueError("Nombre maximum de tours atteint")

        round_name = f"{self.name} - Round {self.current_round}"
        new_round = Round(round_name)

        pairs = self.generate_pairs()

        for player1, player2 in pairs:
            new_round.create_match(player1, player2)

        self.rounds.append(new_round)
        self.current_round += 1

        return new_round

    def has_played_together(self, player1, player2):
        """
        Vérifie si deux joueurs ont déjà joué ensemble dans le tournoi.

        Parcourt tous les rounds et tous les matchs pour détecter si les deux
        joueurs ont déjà été opposés.

        Args:
            player1 (Player): Premier joueur à vérifier
            player2 (Player): Deuxième joueur à vérifier

        Returns:
            bool: True si les joueurs ont déjà joué ensemble, False sinon
        """

        for round in self.rounds:
            for match in round.match_list:
                if player1 in [match.player1, match.player2] and player2 in [match.player1, match.player2]:
                    return True
        return False

    def get_player_score(self, player):

        """
        Calcule le score total d'un joueur dans le tournoi.

        Parcourt tous les rounds et tous les matchs pour additionner les points
        obtenus par le joueur.

        Args:
            player (Player): Le joueur dont on veut calculer le score

        Returns:
            float: Score total du joueur (somme des scores de tous ses matchs)
        """
        total_score = 0

        for round in self.rounds:
            for match in round.match_list:
                if player == match.player1:
                    total_score += match.player1_score
                elif player == match.player2:
                    total_score += match.player2_score

        return total_score

    def even_number_of_players(self):

        """
        Teste si le nombre de joueurs est pair

        Return True si oui, False si non
        """

        if len(self.players) % 2 == 0:
            return True
        else:
            return False
