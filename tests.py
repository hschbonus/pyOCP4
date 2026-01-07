from models.tournament import Tournament
from models.player import Player
from models.round import Round

player_list = [
    Player("Dubois", "Marie", "15/03/1995", "AB123456"),
    Player("Martin", "Lucas", "22/07/1988", "CD789012"),
    Player("Bernard", "Sophie", "08/11/1992", "EF345678"),
    Player("Petit", "Thomas", "30/05/1990", "GH901234"),
    Player("Robert", "Emma", "12/09/1987", "IJ567890"),
    Player("Richard", "Alexandre", "25/01/1994", "KL123456"),
    Player("Durand", "Camille", "18/06/1991", "MN789012"),
    Player("Leroy", "Nicolas", "03/12/1989", "OP345678")
]

tournoi_test = Tournament("Tounoi test", '', '', '', 'test')

for player in player_list:
    tournoi_test.add_player(player)

for pair in tournoi_test.generate_pairs():
    print(pair)

