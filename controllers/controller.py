from tinydb import TinyDB, Query, where
import pprint

class Controller:


    db = TinyDB('db.json')
    #1db.truncate()
    table_joueurs = db.table("joueurs")
    table_tournois = db.table("tournois")


    def __init__(self, view):
        self.view = view

    def get_joueur(self):
        db = TinyDB('db.json')
        joueur = self.view.prompt_joueur()
        self.table_joueurs.insert({'nom_joueur': joueur.nom, 'prenom_joueur': joueur.prenom,
                   'date_de_naissance': joueur.date_de_naissance, 'sexe': joueur.sexe,
                   'classement': joueur.classement
                   })
        pprint.pprint(self.table_joueurs.all())
        return joueur

    def afficher_joueurs(self):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        User = Query()
        print("Liste des Joueurs")

        for joueur in table_joueurs:
            results = str(joueur.doc_id) + " : " + joueur["prenom_joueur"] + " " + \
                      joueur["nom_joueur"] + " (" + joueur["classement"] + ")"
            print(results)

    def update_joueur_classement(self):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        self.afficher_joueurs()
        joueur_id = self.view.prompt_get_id()
        nouveau_classement = self.view.prompt_get_nouveau_classement()

        for joueur in table_joueurs:
            if str(joueur.doc_id) == joueur_id:
                table_joueurs.update({"classement": nouveau_classement}, doc_ids=[joueur.doc_id])
                print("Changement effectué avec succès")

    def cree_tournoi(self):
        db = TinyDB('db.json')
        tournoi = self.view.prompt_tournoi()
        self.table_tournois.insert({'nom_tournoi': tournoi.nom_tournoi, 'lieu': tournoi.lieu, 'date_debut': tournoi.date_debut,
                                   'date_fin': tournoi.date_fin, 'nombre_tours': tournoi.nombre_tours,
                                   'controle_temps': tournoi.controle_du_temps, 'description': tournoi.description
                                   })
        pprint.pprint(self.table_tournois.all())
        return tournoi

    def afficher_liste_tournois(self):
        db = TinyDB('db.json')
        table_tournois = db.table("tournois")
        User = Query()
        print("Liste Des Tournois")

        for tournoi in table_tournois:
            results = str(tournoi.doc_id) + " : " + tournoi["nom_tournoi"] + " " + \
                      tournoi["lieu"] + " (" + tournoi["date_debut"] + ")"
            print(results)

    def print_joueur(self, joueur):
        print(joueur.nom)

    def run(self):
        self.afficher_menu_principal()

    def afficher_menu_principal(self):
        index = self.view.show_menu()
        self.afficher_sous_menu(index)

    def afficher_sous_menu(self, index):
        if index == str(1):
            index2 = self.view.show_menu_joueurs()
            self.afficher_sous_menu_joueurs(index2)
        elif index == str(2):
            index2 = self.view.show_menu_tournois()
            self.afficher_sous_menu_tournois(index2)
        elif index == str(3):
            index2 = self.view.show_menu_match()
            self.afficher_sous_menu_match(index2)
        elif index == str(4):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()

    def afficher_sous_menu_joueurs(self, index):
        if index == str(1):
            self.get_joueur()
        elif index == str(2):
            self.update_joueur_classement()
        elif index == str(3):
            self.afficher_joueurs()
        elif index == str(4):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()
        self.afficher_sous_menu("1")

    def afficher_sous_menu_tournois(self, index):
        if index == str(1):
            self.cree_tournoi()
        elif index == str(2):
            self.afficher_liste_tournois()
        elif index == str(3):
            print("afficher tournoi")
        elif index == str(4):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()
        self.afficher_sous_menu("2")

    def afficher_sous_menu_match(self, index):
        if index == str(1):
            print("saisir resultat")
        elif index == str(2):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()

