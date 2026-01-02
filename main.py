import sys

print("\nBienvenue dans Chess Tournament Manager 2026 !")


def afficher_menu(titre, options):
    print('\n' + titre + '\n' + '-' * len(titre))
    for option in options:
        print(option)

    choix = input('\nVotre choix : ')
    return choix


def menu_principal():

    options = [
        "1. Vers sous-menu 1",
        "2. Vers sous-menu 2",
        "-------------------",
        "3. Quitter"
    ]

    choix = afficher_menu("Menu Principal", options)

    if choix == "1":
        sous_menu1()
    elif choix == "2":
        sous_menu2()
    elif choix == "3":
        print('A bientôt !\n')
        sys.exit()
    else:
        print("Choix invalide !")
        menu_principal()


def sous_menu1():

    options = [
        "1. Sous-choix 11",
        "2. Sous-choix 12",
        "----------------",
        "3. Retourner au menu principal",
        "4. Quitter"
    ]

    choix = afficher_menu("Sous-menu 1", options)

    if choix == "1":
        print(">> Vous avez choisi l'option 11")
    elif choix == "2":
        print(">> Vous avez choisi l'option 12")
    elif choix == "3":
        menu_principal()
    elif choix == "4":
        print('A bientôt !\n')
        sys.exit()
    else:
        print("Choix invalide !")
        sous_menu1()


def sous_menu2():

    options = [
        "1. Sous-choix 21",
        "2. Sous-choix 22",
        "----------------",
        "3. Retourner au menu principal",
        "4. Quitter"
    ]

    choix = afficher_menu("Sous-menu 2", options)

    if choix == "1":
        print(">> Vous avez choisi l'option 21")
    elif choix == "2":
        print(">> Vous avez choisi l'option 22")
    elif choix == "3":
        menu_principal()
    elif choix == "4":
        print('A bientôt !\n')
        sys.exit()
    else:
        print("Choix invalide !")
        sous_menu2()


menu_principal()
