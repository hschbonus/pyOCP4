from models.tournament import Tournament
from models.player import Player
from rich import print

tournoi = Tournament(
    name="Tournoi Paris",
    place="Bordeaux",
    description="Tournoi modifié pour test",
    rounds_nb=6
)

tournoi.current_round = 3

joueur1 = Player("Test", "Alice", "01/01/1990", "AB12345")
joueur2 = Player("Test", "Bob", "02/02/1991", "CD23456")
tournoi.add_player(joueur1)
tournoi.add_player(joueur2)

print(tournoi.players)
tournoi.save_in_json()
