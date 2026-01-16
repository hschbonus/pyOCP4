"""Script de test rapide pour le tournoi avec 6 joueurs."""

from models.tournament import Tournament
from models.player import Player
from datetime import datetime

# Créer un tournoi
tournoi = Tournament(
    name="Tournoi Test",
    place="Paris",
    start_date=datetime.now(),
    end_date="",
    description="Test rapide",
    rounds_nb=2
)

# Ajouter 6 joueurs rapidement
joueurs = [
    Player("Dupont", "Alice", "01/01/1990", "AB12345"),
    Player("Martin", "Bob", "02/02/1991", "CD23456"),
    Player("Bernard", "Charlie", "03/03/1992", "EF34567"),
    Player("Dubois", "David", "04/04/1993", "GH45678"),
    Player("Robert", "Eve", "05/05/1994", "IJ56789"),
    Player("Simon", "Frank", "06/06/1995", "KL67890"),
]

for joueur in joueurs:
    tournoi.add_player(joueur)

print(f"Tournoi créé : {tournoi.name}")
print(f"Nombre de joueurs : {len(tournoi.players)}")
print("\nJoueurs inscrits :")
for joueur in tournoi.players:
    print(f"  - {joueur.firstname}")

# Lancer le premier round
print("\n=== Lancement du Round 1 ===")
round1 = tournoi.create_round()

print("\nMatchs :")
for match in round1.match_list:
    print(match)

# Simuler des résultats aléatoires
import random
for match in round1.match_list:
    result = random.choice(['player1', 'player2', 'draw'])
    match.set_result(result)
    print(f"{match.player1.firstname} vs {match.player2.firstname} → {result}")

round1.mark_as_complete()

# Afficher le classement
print("\n=== CLASSEMENT ===")
players_scores = []
for player in tournoi.players:
    player_score = tournoi.get_player_score(player)
    players_scores.append([player.firstname, player_score])

players_scores.sort(key=lambda x: x[1], reverse=True)

for i, (name, score) in enumerate(players_scores, 1):
    print(f"{i}. {name:<15} || {score}")