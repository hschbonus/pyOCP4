import random
from datetime import datetime
from .player import Player
from .round import Round
from .match import Match


class Tournament:

    def __init__(self,
                 name,
                 place,
                 description,
                 rounds_nb=4):
        """
        Initialise un nouveau tournoi.

        Args:
            name (str): Nom du tournoi.
            place (str): Lieu du tournoi.
            description (str): Description du tournoi.
            rounds_nb (int, optional): Nombre de rounds. Defaults to 4.
        """
        self.name = name
        self.place = place
        self.start_date = datetime.now().replace(microsecond=0)
        self.end_date = None
        self.description = description
        self.rounds = []
        self.rounds_nb = rounds_nb
        self.current_round = 1
        self.players = []

    def __repr__(self):
        """
        Retourne une représentation détaillée du tournoi.

        Returns:
            str: Chaîne formatée avec les informations du tournoi.
        """
        return (f"Tournament(name='{self.name}', place='{self.place}', "
                f"start_date='{self.start_date}', end_date='{self.end_date}', "
                f"rounds_nb={self.rounds_nb}, current_round={self.current_round}, "
                f"players={len(self.players)})")

    def to_dict(self):
        """
        Convertit l'objet Tournament en dictionnaire sérialisable.

        Returns:
            dict: Dictionnaire contenant tous les attributs du tournoi,
                  incluant les joueurs et rounds sérialisés.
        """
        serializable_players = []
        for player in self.players:
            serializable_players.append(player.to_dict())

        serializables_rounds = []
        for round in self.rounds:
            serializables_rounds.append(round.to_dict())

        tournament_dict = {
            'name': self.name,
            'place': self.place,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'description': self.description,
            'rounds': serializables_rounds,
            'rounds_nb': self.rounds_nb,
            'current_round': self.current_round,
            'players': serializable_players
        }
        return tournament_dict

    @classmethod
    def from_dict(cls, tournament_dict):
        """
        Reconstruit un objet Tournament depuis un dictionnaire JSON.
        Gère la désérialisation imbriquée des Players, Rounds et Matchs.
        """
        players = [Player.from_dict(p) for p in tournament_dict["players"]]

        tournament = cls(
            name=tournament_dict["name"],
            place=tournament_dict["place"],
            description=tournament_dict["description"],
            rounds_nb=tournament_dict["rounds_nb"]
        )

        def find_player(national_id):
            for player in players:
                if player.national_id == national_id:
                    return player
            raise ValueError(f"Player with national_id {national_id} not found")

        rounds = []
        for round_dict in tournament_dict["rounds"]:
            round_obj = Round(name=round_dict["name"])

            round_obj.start_date_time = datetime.fromisoformat(round_dict["start_date_time"])

            if round_dict["end_date_time"] and round_dict["end_date_time"] != "None":
                round_obj.end_date_time = datetime.fromisoformat(round_dict["end_date_time"])
            else:
                round_obj.end_date_time = None

            for match_dict in round_dict["match_list"]:
                player1 = find_player(match_dict["player1"])
                player2 = find_player(match_dict["player2"])

                match = Match(
                    player1=player1,
                    player2=player2,
                    player1_score=match_dict["player1_score"],
                    player2_score=match_dict["player2_score"]
                )

                round_obj.match_list.append(match)

            rounds.append(round_obj)

        tournament.players = players
        tournament.rounds = rounds
        tournament.current_round = len(rounds) + 1

        tournament.start_date = datetime.fromisoformat(tournament_dict["start_date"])

        if tournament_dict["end_date"] and tournament_dict["end_date"] != "None":
            tournament.end_date = datetime.fromisoformat(tournament_dict["end_date"])
        else:
            tournament.end_date = None

        return tournament

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

    def check_if_in_tournament_already(self, player):
        """
        Vérifie si un joueur est déjà inscrit au tournoi.

        Args:
            player (Player): Le joueur à vérifier.

        Returns:
            bool: True si le joueur est déjà inscrit, False sinon.
        """
        return player.national_id in [p.national_id for p in self.players]

    @staticmethod
    def create_players_by_id(tournament_dict, national_id):
        """
        Crée un objet Player à partir d'un dictionnaire de tournoi et d'un ID national.

        Args:
            tournament_dict (dict): Dictionnaire contenant les données du tournoi.
            national_id (str): Identifiant national du joueur à créer.

        Returns:
            Player: Instance du joueur trouvé, ou None si non trouvé.
        """
        for player in tournament_dict["players"]:
            if player["national_id"] == national_id:
                player_created = Player(
                    lastname=player["lastname"],
                    firstname=player["firstname"],
                    birth_date=player["birth_date"],
                    national_id=player["national_id"]
                )
                return player_created
        return None

    def mark_as_complete(self):
        """
        Marque le tournoi comme terminé en enregistrant la date de fin.
        """
        self.end_date = datetime.now().replace(microsecond=0)
