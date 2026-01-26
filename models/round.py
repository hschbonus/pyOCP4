from .match import Match
from datetime import datetime


class Round:

    def __init__(self,
                 name,
                 match_list=None):
        """
        Initialise un nouveau round.

        Args:
            name (str): Nom du round.
            match_list (list, optional): Liste des matchs. Defaults to None.
        """
        self.name = name
        self.start_date_time = datetime.now().replace(microsecond=0)
        self.end_date_time = None
        self.match_list = match_list if match_list is not None else []

    def __repr__(self):
        """
        Retourne une représentation du round.

        Returns:
            str: Nom du round.
        """
        return f"{self.name}"

    def to_dict(self):
        """
        Convertit l'objet Round en dictionnaire sérialisable.

        Returns:
            dict: Dictionnaire contenant les attributs du round et ses matchs.
        """
        serializable_match_list = []
        for match in self.match_list:
            serializable_match_list.append(match.to_dict())

        round_dict = {
            'name': self.name,
            'start_date_time': str(self.start_date_time),
            'end_date_time': str(self.end_date_time),
            'match_list': serializable_match_list
        }
        return round_dict

    @classmethod
    def from_dict(cls, round_dict):
        """
        Crée une instance de Round à partir d'un dictionnaire.

        Args:
            round_dict (dict): Dictionnaire contenant les données du round.

        Returns:
            Round: Nouvelle instance de Round avec ses matchs.
        """
        round = cls(
            name=round_dict["name"],
            match_list=[Match.from_dict(m) for m in round_dict["match_list"]]
        )

        round.start_date_time = datetime.fromisoformat(round_dict["start_date_time"])
        round.end_date_time = 'None'
        return round

    def create_match(self, player1, player2):
        """
        Crée un nouveau match entre deux joueurs et l'ajoute au round.

        Args:
            player1 (Player): Premier joueur du match.
            player2 (Player): Deuxième joueur du match.

        Returns:
            Match: Instance du match créé.
        """
        match = Match(player1, player2)
        self.match_list.append(match)
        return match

    def mark_as_complete(self):
        """
        Marque le round comme terminé en enregistrant la date et heure de fin.
        """
        self.end_date_time = datetime.now().replace(microsecond=0)
