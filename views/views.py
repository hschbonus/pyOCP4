from rich import print
from models.tournament import Tournament
from models.player import Player

BANNER_LENGTH = 50


def display_menu(titre, options, tournoi: Tournament):
    """
    Affiche un menu avec titre, options et informations du tournoi en cours.

    Args:
        titre (str): Titre du menu à afficher.
        options (list): Liste des options du menu.
        tournoi (Tournament): Tournoi en cours (peut être None).

    Returns:
        str: Choix de l'utilisateur.
    """
    banner(titre)

    if tournoi:
        print(f"Tournoi en cours : {tournoi.name}")
        print(f"Date de création : {tournoi.start_date}")
        print(f"Nombre de joueurs inscrits : {len(tournoi.players)}\n")

    for option in options:
        print(option)

    choix = input('\nVotre choix : ')
    return choix


def tournament_input():
    """
    Demande à l'utilisateur les informations pour créer un tournoi.

    Returns:
        dict: Dictionnaire contenant name, place, description et optionnellement rounds_nb.
    """
    name = input('\nNom : ')
    place = input('Lieu : ')
    description = input('Description : ')
    rounds_nb = input('Nombre de rondes (par défaut: 4): ')

    if rounds_nb == '':
        return {'name': name,
                'place': place,
                'description': description,
                }
    else:
        return {'name': name,
                'place': place,
                'description': description,
                'rounds_nb': rounds_nb
                }


def id_input():
    """
    Demande à l'utilisateur de saisir un identifiant national.

    Returns:
        str: Identifiant national saisi.
    """
    national_id = input('ID National : ')
    return national_id


def player_data_input():
    """
    Demande à l'utilisateur les données d'un joueur.

    Returns:
        tuple: (lastname, firstname, birthdate) saisis par l'utilisateur.
    """
    lastname = input('\nNom de famille : ')
    firstname = input('Prénom : ')
    birthdate = input('Date de naissance : ')

    return lastname, firstname, birthdate


def update_player():
    """
    Demande les nouvelles données pour mettre à jour un joueur existant.

    Returns:
        tuple: (lastname, firstname, birthdate) saisis par l'utilisateur.
    """
    print("\nJoueur présent dans la BDD, modifier ses données ? :")
    lastname, firstname, birthdate = player_data_input()
    return lastname, firstname, birthdate


def create_player():
    """
    Demande les données pour créer un nouveau joueur.

    Returns:
        tuple: (lastname, firstname, birthdate) saisis par l'utilisateur.
    """
    print("\nJoueur inconnu de la BDD, entrez les données suivantes :")
    lastname, firstname, birthdate = player_data_input()
    return lastname, firstname, birthdate


def player_added(name, tournoi_name):
    """
    Affiche un message de confirmation d'inscription d'un joueur.

    Args:
        name (str): Nom du joueur inscrit.
        tournoi_name (str): Nom du tournoi.
    """
    print(f'\n{name} a bien été inscrit(e) au tournoi {tournoi_name} !')


def all_matchs_from_round_display(round):
    """
    Affiche tous les matchs d'un round.

    Args:
        round (Round): Le round dont on veut afficher les matchs.
    """
    banner(f'Matchs de {round.name}')

    for match in round.match_list:
        print(match)


def winner_input(match):
    """
    Demande à l'utilisateur le résultat d'un match.

    Args:
        match (Match): Le match pour lequel saisir le résultat.

    Returns:
        str: Choix de l'utilisateur ('1', '2' ou '3').
    """
    print(f'\nRésultat du match entre {match.player1.firstname} et {match.player2.firstname}:')
    print(f'1 : {match.player1.firstname} est vainqueur')
    print(f'2 : {match.player2.firstname} est vainqueur')
    print('3 : Egalité')
    winner = input('\nRésultat : ')
    return winner


def leaderboard_display(tournoi):
    """
    Affiche le classement des joueurs du tournoi.

    Affiche le classement intermédiaire ou final selon l'état du tournoi.

    Args:
        tournoi (Tournament): Le tournoi dont on veut afficher le classement.
    """
    players_scores = []
    COL_LEN = 20

    for player in tournoi.players:
        player_score = tournoi.get_player_score(player)
        players_scores.append([player.firstname, player_score])
    players_scores.sort(key=lambda x: x[1], reverse=True)

    if tournoi.current_round < tournoi.rounds_nb + 1:
        print(f"\nCLASSEMENT A L'ISSUE DU ROUND {tournoi.current_round - 1}\n")
    else:
        print("\nCLASSEMENT FINAL\n")
    i = 0
    for i in range(0, len(tournoi.players)):
        print(f"{i + 1}. {players_scores[i][0]}{' ' * (COL_LEN - len(players_scores[i][0]))}|| {players_scores[i][1]}")


def banner(text):
    """
    Affiche une bannière formatée avec un texte centré.

    Args:
        text (str): Texte à afficher dans la bannière.
    """
    print()
    print('=' * BANNER_LENGTH)
    space = ((BANNER_LENGTH - 4) - len(text)) / 2
    print('=' * int(space) + '  ' + text + '  ' + '=' * int(space))
    print('=' * BANNER_LENGTH)
    print()


def players_report(tournoi):
    """
    Affiche la liste des joueurs inscrits au tournoi.

    Args:
        tournoi (Tournament): Le tournoi dont on veut afficher les joueurs.
    """
    print(f"\nJoueurs inscrits dans le tournoi {tournoi.name} :\n")
    for player in tournoi.players:
        print(player)


def rounds_and_matchs_report(tournoi):
    """
    Affiche la liste de tous les rounds et matchs du tournoi.

    Args:
        tournoi (Tournament): Le tournoi dont on veut afficher les rounds.
    """
    print("Liste des rounds et des matchs :\n")
    for round in tournoi.rounds:
        print(f"\n{round}\n")
        for match in round.match_list:
            print(f"    {match}")


def tournament_already_exists(name):
    """
    Affiche un message d'erreur si un tournoi existe déjà.

    Args:
        name (str): Nom du tournoi en doublon.
    """
    print(f"\nLe tournoi {name} existe déjà, veuillez entrer un autre nom svp.")


def resume_tournament(tournoi):
    """
    Affiche un message de reprise d'un tournoi en cours.

    Args:
        tournoi (Tournament): Le tournoi repris.
    """
    print(f"\nReprise du tournoi en cours : {tournoi.name}")
    print(f"Round {tournoi.current_round - 1} en cours.")


def tournament_is_over():
    """Affiche un message indiquant que le tournoi est terminé."""
    print("Ce tournoin est déjà terminé !")


def all_players_in_db_report(data):
    """
    Affiche la liste de tous les joueurs enregistrés dans la base de données.

    Args:
        data (dict): Données de la base contenant la liste des joueurs.
    """
    if data["players"]:
        banner("LISTE DES JOUEURS")
        print(f"Total : {len(data["players"])}\n")
        for player_dict in data["players"]:
            player = Player.from_dict(player_dict)
            print(player)
        print()
    else:
        print("\nAucun joueur à afficher !\n")


def all_tournaments_in_db_report(data):
    """
    Affiche la liste de tous les tournois enregistrés dans la base de données.

    Args:
        data (dict): Données de la base contenant la liste des tournois.
    """
    if len(data["tournaments"]) != 0:
        banner("LISTE DES TOURNOIS")
        for tournament in data["tournaments"]:
            print(tournament["name"])
            print(f"Date de création : {tournament["start_date"]}")
            if tournament["end_date"] == "None":
                print("En cours")
            else:
                print(f"Date de fin : {tournament["end_date"]}\n")
    else:
        print("\nAucun tournoi à afficher !\n")


def exit():
    """Affiche un message de sortie de l'application."""
    print("A bientôt !\n")


def invalid():
    """Affiche un message d'erreur pour un choix invalide."""
    print("Choix invalide !\n")


def player_not_even():
    """Affiche un message d'erreur si le nombre de joueurs n'est pas pair."""
    print("\nLe nombre de joueurs doit être pair !")


def no_players():
    """Affiche un message d'erreur si aucun joueur n'est inscrit."""
    print("\nLe tournoi ne peut pas commencer sans joueurs.")
