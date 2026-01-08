from models.player import Player
from models.tournament import Tournament

# Créer 8 joueurs
alice = Player("Dupont", "Alice", "1990-01-15", "AA00001")
bob = Player("Martin", "Bob", "1985-03-22", "BB00002")
charlie = Player("Durand", "Charlie", "1992-07-10", "CC00003")
david = Player("Bernard", "David", "1988-11-05", "DD00004")
emma = Player("Petit", "Emma", "1995-04-18", "EE00005")
frank = Player("Robert", "Frank", "1987-09-30", "FF00006")
grace = Player("Richard", "Grace", "1991-12-25", "GG00007")
henry = Player("Moreau", "Henry", "1989-06-14", "HH00008")

# Créer le tournoi
tournament = Tournament("Test Tournament", "Paris", "2025-01-10", "2025-01-12", "Test")

# Ajouter les joueurs
for player in [alice, bob, charlie, david, emma, frank, grace, henry]:
    tournament.add_player(player)

# ===== ROUND 1 =====
print("=== ROUND 1 ===")
round1 = tournament.create_round()
print(f"Paires générées : {[(m.player1.first_name, m.player2.first_name) for m in round1.match_list]}")

# Simuler des résultats pour le Round 1
round1.match_list[0].set_result('player1')  # Alice bat son adversaire
round1.match_list[1].set_result('draw')     # Match nul
round1.match_list[2].set_result('player2')  # Le player2 gagne
round1.match_list[3].set_result('player1')  # Le player1 gagne

# ===== ROUND 2 =====
print("\n=== ROUND 2 ===")
print("Scores actuels :")
for player in tournament.players:
    score = tournament.get_player_score(player)
    print(f"  {player.first_name}: {score}")

round2 = tournament.create_round()
print(f"Paires générées : {[(m.player1.first_name, m.player2.first_name) for m in round2.match_list]}")

# Simuler des résultats pour le Round 2
round2.match_list[0].set_result('player1')
round2.match_list[1].set_result('player2')
round2.match_list[2].set_result('draw')
round2.match_list[3].set_result('player1')

# ===== ROUND 3 =====
print("\n=== ROUND 3 ===")
print("Scores actuels :")
for player in tournament.players:
    score = tournament.get_player_score(player)
    print(f"  {player.first_name}: {score}")

round3 = tournament.create_round()
print(f"Paires générées : {[(m.player1.first_name, m.player2.first_name) for m in round3.match_list]}")

# Vérifier qu'il n'y a pas de doublons
print("\n=== VÉRIFICATION DES DOUBLONS ===")
for round_obj in tournament.rounds:
    for match in round_obj.match_list:
        p1 = match.player1.first_name
        p2 = match.player2.first_name
        print(f"{p1} vs {p2}")