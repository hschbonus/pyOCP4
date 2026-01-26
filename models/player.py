class Player:

    def __init__(self, lastname, firstname, birth_date, national_id):
        """
        Initialise un nouveau joueur.

        Args:
            lastname (str): Nom de famille du joueur.
            firstname (str): Prénom du joueur.
            birth_date (str): Date de naissance du joueur.
            national_id (str): Identifiant national unique du joueur.
        """
        self.lastname = lastname
        self.firstname = firstname
        self.birth_date = birth_date
        self.national_id = national_id

    def __str__(self):
        """
        Retourne une représentation lisible du joueur.

        Returns:
            str: Chaîne formatée avec nom, prénom, date de naissance et ID.
        """
        return (f"{self.lastname} {self.firstname}, "
                f"né(e) le {self.birth_date}, ID: {self.national_id}")

    def __repr__(self):
        """
        Retourne une représentation courte du joueur.

        Returns:
            str: Prénom et nom du joueur.
        """
        return f"{self.firstname} {self.lastname}"

    def to_dict(self):
        """
        Convertit l'objet Player en dictionnaire sérialisable.

        Returns:
            dict: Dictionnaire contenant les attributs du joueur.
        """
        player_dict = {
            'lastname': self.lastname,
            'firstname': self.firstname,
            'birth_date': self.birth_date,
            'national_id': self.national_id,
        }
        return player_dict

    @classmethod
    def from_dict(cls, player_dict):
        """
        Crée une instance de Player à partir d'un dictionnaire.

        Args:
            player_dict (dict): Dictionnaire contenant les données du joueur.

        Returns:
            Player: Nouvelle instance de Player.
        """
        player = cls(**player_dict)
        return player
