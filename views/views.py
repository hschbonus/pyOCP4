from datetime import datetime
# from controllers import controllers
from models.tournament import Tournament

BANNER_LENGTH = 50


def display_menu(titre, options, tournoi: Tournament):

    banner(titre)

    if tournoi:
        print(f'Tournoi en cours : {tournoi.name}')
        print(f'Nombre de joueurs inscrits : {len(tournoi.players)}\n')

    for option in options:
        print(option)

    choix = input('\nVotre choix : ')
    return choix


def tournament_input():
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


def player_input():
    lastname = input('\nNom de famille : ')
    firstname = input('Prénom : ')
    birthdate = input('Date de naissance : ')
    national_id = input('ID National : ')

    return {'lastname': lastname,
            'firstname': firstname,
            'birth_date': birthdate,
            'national_id': national_id,
            }


def player_added(name, tournoi_name):
    print(f'\n{name} a bien été inscrit(e) au tournoi {tournoi_name} !\n')


def all_matchs_from_round_display(round):

    banner(f'Matchs de {round.name}')

    for match in round.match_list:
        print(match)


def winner_input(match):
    print('\nRésultat du match entre :')
    print(f'1 : {match.player1.firstname} est vainqueur')
    print(f'2 : {match.player2.firstname} est vainqueur')
    print('3 : Egalité')
    winner = input('\nRésultat : ')
    return winner


def leaderboard_display(tournoi):

    players_scores = []
    COLUMN_LENGTH = 20

    for player in tournoi.players:
        player_score = tournoi.get_player_score(player)
        players_scores.append([player.firstname, player_score])
    players_scores.sort(key=lambda x: x[1], reverse=True)

    if tournoi.current_round - 1 < tournoi.rounds_nb:
        print(f"\nCLASSEMENT A L'ISSUE DU ROUND {tournoi.current_round - 1}\n")
    else:
        print("\nCLASSEMENT FINAL\n")
    i = 0
    for i in range(0, len(tournoi.players)):
        print(str(i) + ". " + players_scores[i][0] + ' ' * (COLUMN_LENGTH - len(players_scores[i][0])) + '||  ' +
              str(players_scores[i][1]))


def banner(text):

    print()
    print('=' * BANNER_LENGTH)
    space = ((BANNER_LENGTH - 4) - len(text)) / 2
    print('=' * int(space) + '  ' + text + '  ' + '=' * int(space))
    print('=' * BANNER_LENGTH)
    print()


def players_report(tournoi):

    print(f"\nJoueurs inscrits dans le tournoi {tournoi.name} :\n")
    players_copy = tournoi.players
    for player in players_copy:
        print(player.firstname)


def rounds_and_matchs_report(tournoi):

    print("Liste des rounds et des matchs :\n")
    for round in tournoi.rounds:
        print(f"\n{round}\n")
        for match in round.match_list:
            print(f"    {match}")
