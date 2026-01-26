from models.player import Player
from models.tournament import Tournament

alice = Player("Dupont", "Alice", "1990-01-15", "AA00001")
bob = Player("Martin", "Bob", "1985-03-22", "BB00002")
charlie = Player("Durand", "Charlie", "1992-07-10", "CC00003")
david = Player("Bernard", "David", "1988-11-05", "DD00004")
emma = Player("Petit", "Emma", "1995-04-18", "EE00005")
frank = Player("Robert", "Frank", "1987-09-30", "FF00006")
grace = Player("Richard", "Grace", "1991-12-25", "GG00007")
henry = Player("Moreau", "Henry", "1989-06-14", "HH00008")

tournament = Tournament("Test Tournament", "Paris", "Test")

for player in [alice, bob, charlie, david, emma, frank, grace, henry]:
    tournament.add_player(player)

print("=== ROUND 1 ===")
round1 = tournament.create_round()
print(f"Paires générées : {[(m.player1.firstname, m.player2.firstname) for m in round1.match_list]}")

round1.match_list[0].set_result('1')
round1.match_list[1].set_result('3')
round1.match_list[2].set_result('2')
round1.match_list[3].set_result('1')

print("\n=== ROUND 2 ===")
print("Scores actuels :")
for player in tournament.players:
    score = tournament.get_player_score(player)
    print(f"  {player.firstname}: {score}")

round2 = tournament.create_round()
print(f"Paires générées : {[(m.player1.firstname, m.player2.firstname) for m in round2.match_list]}")

round2.match_list[0].set_result('1')
round2.match_list[1].set_result('2')
round2.match_list[2].set_result('3')
round2.match_list[3].set_result('1')

print("\n=== ROUND 3 ===")
print("Scores actuels :")
for player in tournament.players:
    score = tournament.get_player_score(player)
    print(f"  {player.firstname}: {score}")

round3 = tournament.create_round()
print(f"Paires générées : {[(m.player1.firstname, m.player2.firstname) for m in round3.match_list]}")

print(tournament.rounds)
