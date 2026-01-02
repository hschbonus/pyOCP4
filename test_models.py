from models.player import Player
from models.tournament import Tournament

player1 = Player("Dupont", "Marie", "1995-03-15", "AB12345")
player2 = Player("Martin", "Jean", "1990-05-20", "CD67890")

tournament = Tournament("Championnat",
                        "Paris",
                        "2025-01-10",
                        "2025-01-12",
                        "Test")

tournament.add_player(player1)
tournament.add_player(player2)

print(f"Nombre de joueurs: {len(tournament.players)}")
print(f"Round actuel: {tournament.current_round}")
for player in tournament.players:
    print(player)
