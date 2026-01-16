import sys
from views import views
from models import Tournament, Player


def main_menu():

    options = [
        "1. Créer un nouveau tournoi",
        "-------------------",
        "2. Quitter"
    ]

    choix = views.display_menu("MENU PRINCIPAL", options, '')

    if choix == "1":
        tournoi = create_tournament()
        tournoi.save_in_json()
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
        "2. Ajouter tous les joueurs du JSON",
        "3. Commencer le tournoi",
        "4. Consulter la liste des joueurs",
        "5. Consulter la liste des rounds et matchs",
        "-------------------",
        "6. Retour au menu principal",
        "7. Quitter le programme"
    ]

    choix = views.display_menu("MENU TOURNOI", options, tournoi)

    if choix == "1":
        infos_player = views.player_input()
        new_player = add_player(infos_player, tournoi)
        new_player.save_in_json()
        tournoi.save_in_json()
        tournament_menu(tournoi)

    elif choix == "2":
        infos_players = Player.load_from_json()
        for infos_player in infos_players:
            add_player(infos_player, tournoi)
        tournoi.save_in_json()
        tournament_menu(tournoi)

    elif choix == "3":
        if tournoi.even_number_of_players():
            start_tournament(tournoi)
        else:
            raise ValueError('Le nombre de joueurs inscrits doit être pair !')
        tournament_menu(tournoi)

    elif choix == "4":
        views.players_report(tournoi)
        tournament_menu(tournoi)

    elif choix == "5":
        views.rounds_and_matchs_report(tournoi)
        tournament_menu(tournoi)

    elif choix == "6":
        main_menu()

    elif choix == "7":
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
        tournoi.save_in_json()
        views.all_matchs_from_round_display(round)
        for match in round.match_list:
            winner = views.winner_input(match)
            match.set_result(winner)
        round.mark_as_complete()
        views.leaderboard_display(tournoi)


def add_player(infos_player, tournoi):
    player = Player(**infos_player)
    tournoi.add_player(player)
    views.player_added(player.firstname, tournoi.name)
    tournoi.save_in_json()
    return player
