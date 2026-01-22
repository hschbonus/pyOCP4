import sys
import json
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
        player = save_player(national_id)
        add_player_to_tournament(player, tournoi)
        save_tournament(tournoi)
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
        main_menu()

    elif choix == "6":
        print('A bientôt !\n')
        sys.exit()

    elif choix == "add all":
        data = load_all()
        for player in data["players"]:
            player_to_add = Player(**player)
            add_player_to_tournament(player_to_add, tournoi)
        save_tournament(tournoi)
        tournament_menu(tournoi)

    else:
        print("Choix invalide !")
        tournament_menu(tournoi)


def create_tournament():
    data = load_all()
    infos_tournoi = views.tournament_input()
    while infos_tournoi["name"] in [tournament["name"] for tournament in data["tournaments"]]:
        views.tournament_already_exists(infos_tournoi["name"])
        infos_tournoi = views.tournament_input()
    tournoi = Tournament(**infos_tournoi)
    return tournoi


def start_tournament(tournoi):
    while len(tournoi.rounds) < tournoi.rounds_nb:
        round = tournoi.create_round()
        views.all_matchs_from_round_display(round)
        save_tournament(tournoi)
        for match in round.match_list:
            winner = views.winner_input(match)
            match.set_result(winner)
            save_tournament(tournoi)
        round.mark_as_complete()
        views.leaderboard_display(tournoi)


def add_player_to_tournament(player, tournoi):
    if not tournoi.check_if_in_tournament_already(player):
        tournoi.add_player(player)
    save_tournament(tournoi)
    views.player_added(player.firstname, tournoi.name)


def save_tournament(tournament_to_save):
    data = load_all()
    tournament_dict = tournament_to_save.to_dict()
    check_if_players_updates(data, tournament_to_save)
    for tournoi in data["tournaments"]:
        if tournament_to_save.name == tournoi["name"]:
            tournoi['rounds'] = tournament_dict["rounds"]
            tournoi['rounds_nb'] = tournament_dict["rounds_nb"]
            tournoi['current_round'] = tournament_dict["current_round"]
            tournoi['players'] = tournament_dict["players"]
            break
    else:
        data["tournaments"].append(tournament_dict)

    with open('data/db.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def check_if_players_updates(data, tournoi):
    all_ids = [player["national_id"] for player in data["players"]]
    for player in tournoi.players:
        if player.national_id in all_ids:
            i = all_ids.index(player.national_id)
            player.lastname = data["players"][i]["lastname"]
            player.firstname = data["players"][i]["firstname"]
            player.birth_date = data["players"][i]["birth_date"]


def load_all():
    with open('data/db.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def mark_as_current(tournoi):

    pass


def save_player(national_id):
    data = load_all()
    for player_dict in data["players"]:
        if national_id == player_dict["national_id"]:
            lastname, firstname, birthdate = views.update_player()
            if lastname:
                player_dict["lastname"] = lastname
            if firstname:
                player_dict["firstname"] = firstname
            if birthdate:
                player_dict["birth_date"] = birthdate

            with open('data/db.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            player = Player.from_dict(player_dict)
            return player

    else:
        lastname, firstname, birthdate = views.create_player()
        new_player = Player(
            lastname, firstname, birthdate, national_id
        )
        new_player_dict = new_player.to_dict()
        data["players"].append(new_player_dict)

        with open('data/db.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return new_player
