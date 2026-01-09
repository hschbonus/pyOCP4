import sys
from views import views
from models.tournament import Tournament
from models.player import Player


def main_menu():

    options = [
        "1. Créer un nouveau tournoi",
        "-------------------",
        "2. Quitter"
    ]

    choix = views.display_menu("MENU PRINCIPAL", options, '')

    if choix == "1":
        tournoi = create_tournament()
        tournament_menu(tournoi)

    elif choix == "2":
        print('A bientôt !\n')
        sys.exit()
    else:
        print("Choix invalide !")
        main_menu()


def tournament_menu(tournoi: Tournament):

    options = [
        "1. Ajouter un joueur",
        "2. Commencer le tournoi",
        "3. Afficher la liste des joueurs",
        "4. Afficher la liste des rounds et matchs",
        "-------------------",
        "5. Quitter"
    ]

    choix = views.display_menu("MENU TOURNOI", options, tournoi)

    if choix == "1":
        infos_player = views.player_input()
        player = Player(**infos_player)
        tournoi.add_player(player)
        views.player_added(player.firstname, tournoi.name)
        tournament_menu(tournoi)

    elif choix == "2":
        if tournoi.even_number_of_players():
            start_tournament(tournoi)
        else:
            raise ValueError('Le nombre de joueurs inscrits doit être pair !')
        tournament_menu(tournoi)

    elif choix == "3":
        views.players_report(tournoi)
        tournament_menu(tournoi)

    elif choix == "4":
        views.rounds_and_matchs_report(tournoi)
        tournament_menu(tournoi)

    elif choix == "5":
        print('A bientôt !\n')
        sys.exit()
    else:
        print("Choix invalide !")
        tournament_menu(tournoi)


def create_tournament():
    infos_tournoi = views.tournament_input()
    tournoi = Tournament(**infos_tournoi)
    return tournoi


def start_tournament(tournoi):
    while len(tournoi.rounds) < tournoi.rounds_nb:
        round = tournoi.create_round()
        views.all_matchs_from_round_display(round)
        for match in round.match_list:
            winner = views.winner_input(match)
            match.set_result(winner)
        round.mark_as_complete()
        views.leaderboard_display(tournoi)
