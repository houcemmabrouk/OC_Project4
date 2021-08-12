from models.joueur import Joueur
from models.tournoi import Tournoi
from tinydb import TinyDB, Query, where
from controllers.controller import Controller
import datetime


class View:

    db = TinyDB('db.json')
    #1db.truncate()
    table_joueurs = db.table("joueurs")
    table_tournois = db.table("tournois")
    # Vues Menu
    def show_menu(self):
        print("Joueurs..........................entrez 1")
        print("Tournois.........................entrez 2")
        print("Match............................entrez 3")
        print("Quitter..........................entrez Q")
        choix = input("Entrez Votre Choix")
        return choix

    def show_menu_joueurs(self):
        print("Créer Joueurs....................entrez 1")
        print("Modifier Classement..............entrez 2")
        print("Afficher Joueurs.................entrez 3")
        print("Revenir Menu Principal...........entrez 4")
        print("Quitter..........................entrez Q")
        choix = input("Entrez Votre Choix")
        return choix

    def show_menu_tournois(self):
        print("Créer Tournois...................entrez 1")
        print("Afficher Liste Tournois..........entrez 2")
        print("Afficher Tournoi.................entrez 3")
        print("Revenir Menu Principal...........entrez 4")
        print("Quitter..........................entrez Q")
        choix = input("Entrez Votre Choix")
        return choix

    def show_menu_match(self):
        print("Saisir Resultat..................entrez 1")
        print("Revenir Menu Principal...........entrez 2")
        print("Quitter..........................entrez Q")
        choix = input("Entrez Votre Choix")
        return choix

    def prompt_joueur(self):
        nom_joueur = input("nom joueur")
        prenom_joueur = input("prenom joueur")
        date_de_naissance = input("date_de_naissance")
        sexe = input("sexe")
        classement = input("classement")
        joueur = Joueur(nom_joueur, prenom_joueur, date_de_naissance, sexe, classement)
        return joueur

    def prompt_get_id(self):
        joueur_id = input("Entrez l'identifiant du joueur que vous souhaitez modifier : ")
        return joueur_id

    def prompt_get_nouveau_classement(self):
        nouveau_classement = input("Entrez le nouveau classement du joueur : ")
        return nouveau_classement

    def prompt_tournoi(self):
        nom_tournoi = input("Entrez le nom du tournoi : ")
        lieu_du_tournoi = input("Entrez le lieu du tournoi : ")
        date_debut = input("Entrez la date du debut du tournoi : ")
        date_fin = input("Entrez la date de fin du tournoi : ")
        nombre_de_tours = input("Entrez le nombre de tours : ")
        self.indices_joueurs = []
        while len(self.indices_joueurs) < 8:
            joueur = input("Entrez l'indice du Joueur que vous souhaitez ajouter : ")
            if joueur not in self.indices_joueurs:
                if self.joueurs_disponibles(joueur) == True:
                    self.indices_joueurs.append(joueur)
                else:
                    print("Cet identifiant ne correspond à aucun joueur")
            else:
                print("Ce joueur à deja été ajouté au tournoi")
        print(self.indices_joueurs)
        #tournee = input("Entrez la tournee : ")
        #joueurs_tournois = input("Entrez les indices des joueurs : ")
        controle_du_temps = input("Entrez le controle du temps : ")
        description_tournoi = input("Entrez une description pour le tournoi : ")
        tournoi = Tournoi(nom_tournoi, lieu_du_tournoi, date_debut, date_fin, nombre_de_tours,
                          controle_du_temps, description_tournoi
                          )

        return tournoi

    def joueurs_disponibles(self, joueur_id):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        User = Query()
        for joueur in table_joueurs:
            if str(joueur.doc_id) == joueur_id:
                return True