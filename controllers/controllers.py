import sys
import json
from views import views
from models import Tournament, Player


def start():
    current_tournament = get_current_tournament()
    if current_tournament and len(current_tournament.rounds) != 0:
        views.resume_tournament(current_tournament)
        resume_tournament_menu(current_tournament)

    elif current_tournament and len(current_tournament.rounds) == 0:
        views.resume_tournament(current_tournament)
        tournament_menu(current_tournament)

    else:
        main_menu()


def main_menu():

    options = [
        "1. Créer un nouveau tournoi",
        "2. Consulter la liste des joueurs",
        "3. Consulter la liste des tournois",
        "-------------------",
        "4. Quitter"
    ]

    choix = views.display_menu("MENU PRINCIPAL", options, '')

    if choix == "1":
        tournoi = create_tournament()
        save_tournament(tournoi)
        tournament_menu(tournoi)

    elif choix == "2":
        data = load_all()
        views.all_players_in_db_report(data)
        main_menu()

    elif choix == "3":
        data = load_all()
        views.all_tournaments_in_db_report(data)
        main_menu()

    elif choix == "4":
        views.exit()
        sys.exit()
    else:
        views.invalid()
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
        tournament_start_check(tournoi)
        start_tournament(tournoi)

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


def resume_tournament_menu(tournoi: Tournament):

    options = [
        "1. Continuer le tournoi",
        "2. Consulter la liste des joueurs",
        "3. Consulter la liste des rounds et matchs",
        "-------------------",
        "4. Quitter le programme"
    ]

    choix = views.display_menu("MENU TOURNOI", options, tournoi)

    if choix == "1":
        tournament_start_check(tournoi)
        resume_tournament(tournoi)

    elif choix == "2":
        views.players_report(tournoi)
        resume_tournament_menu(tournoi)

    elif choix == "3":
        views.rounds_and_matchs_report(tournoi)
        resume_tournament_menu(tournoi)

    elif choix == "4":
        print('A bientôt !\n')
        sys.exit()

    else:
        print("Choix invalide !")
        resume_tournament_menu(tournoi)


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
    tournoi.mark_as_complete()
    save_tournament(tournoi)
    main_menu(tournoi)


def resume_tournament(tournoi):
    """
    Reprend un tournoi là où il s'était arrêté.
    Si le dernier round n'est pas terminé, on le termine.
    Puis on continue avec les rounds suivants.
    """
    if tournoi.rounds and tournoi.rounds[-1].end_date_time is None:
        current_round = tournoi.rounds[-1]
        views.all_matchs_from_round_display(current_round)

        for match in current_round.match_list:
            winner = views.winner_input(match)
            match.set_result(winner)

        current_round.mark_as_complete()
        save_tournament(tournoi)

        views.leaderboard_display(tournoi)

    while len(tournoi.rounds) < tournoi.rounds_nb:
        round = tournoi.create_round()
        save_tournament(tournoi)
        views.all_matchs_from_round_display(round)

        for match in round.match_list:
            winner = views.winner_input(match)
            match.set_result(winner)

        round.mark_as_complete()
        save_tournament(tournoi)
        views.leaderboard_display(tournoi)
    tournoi.mark_as_complete()
    save_tournament(tournoi)
    main_menu()


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
            tournoi['end_date'] = tournament_dict["end_date"]
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


def get_current_tournament():
    data = load_all()
    end_dates = [t["end_date"] for t in data["tournaments"]]
    if "None" in end_dates:
        i = end_dates.index("None")
        tournoi = Tournament.from_dict(data["tournaments"][i])
        return tournoi


def tournament_start_check(tournoi):
    if len(tournoi.players) % 2 != 0:
        views.player_not_even()
        tournament_menu(tournoi)
    elif len(tournoi.players) == 0:
        views.no_players()
        tournament_menu(tournoi)
    elif len(tournoi.rounds) >= tournoi.rounds_nb:
        views.tournament_is_over()
    else:
        pass
