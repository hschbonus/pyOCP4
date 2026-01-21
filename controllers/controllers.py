import sys
import json
from views import views
from models import Tournament, Player, Round


def main_menu():

    options = [
        "1. Créer un nouveau tournoi",
        "-------------------",
        "2. Quitter"
    ]

    choix = views.display_menu("MENU PRINCIPAL", options, '')

    if choix == "1":
        tournoi = create_tournament()
        save_tournament(tournoi)
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
        "3. Consulter la liste des joueurs",
        "4. Consulter la liste des rounds et matchs",
        "-------------------",
        "5. Retour au menu principal",
        "6. Quitter le programme"
    ]

    choix = views.display_menu("MENU TOURNOI", options, tournoi)

    if choix == "1":
        data = load_all()
        national_id = views.id_input()
        for player in data["players"]:
            if player["national_id"] == national_id:
                player = update_player(player)
                add_player_to_tournament(player, tournoi)
                tournament_menu(tournoi)
                return True
        new_player = create_player(national_id)
        data["players"].append(new_player)
        add_player_to_tournament(new_player, tournoi)
        tournament_menu(tournoi)
        return False

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
        main_menu()

    elif choix == "6":
        print('A bientôt !\n')
        sys.exit()

    elif choix == "add all":
        data = load_all()
        for player in data["players"]:
            add_player_to_tournament(player, tournoi)
        save_all(data)
        tournament_menu(tournoi)

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


def add_player_to_tournament(player, tournoi):
    tournoi.add_player(player)
    save_tournament(tournoi)
    views.player_added(player.firstname, tournoi.name)


# def save_player(player_to_save):
#     pass


def save_tournament(tournament_to_save):
    try:
        data = load_all()
        tournament_in_dict = tournament_to_save.to_dict()
        for tournoi in data["tournaments"]:
            if tournament_to_save.name in tournoi["name"]:
                tournoi['rounds'] = tournament_in_dict["rounds"]
                tournoi['rounds_nb'] = tournament_to_save.rounds_nb
                tournoi['current_round'] = tournament_to_save.current_round
                tournoi['players'] = tournament_in_dict["players"]
        else:
            data["tournaments"].append(tournament_in_dict)

    except UnboundLocalError:
        pass

    with open('data/db.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_all():
    with open('data/db.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def mark_as_current(tournoi):
    pass


def update_player(player):
    lastname, firstname, birthdate = views.update_player()
    if lastname:
        player["lastname"] = lastname
    if lastname:
        player["firstname"] = firstname
    if lastname:
        player["birth_date"] = birthdate
    return player


def create_player(national_id):
    lastname, firstname, birthdate = views.create_player()
    new_player = Player(
        lastname, firstname, birthdate, national_id
    )
    return new_player
