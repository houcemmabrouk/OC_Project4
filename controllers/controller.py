from tinydb import TinyDB, Query, where
import pprint
from typing import List
from models.joueur import Joueur
from models.tournoi import Tournoi


class Controller:


    db = TinyDB('db.json')

    table_joueurs = db.table("joueurs")
    table_tournois = db.table("tournois")
    #table_tournois.truncate()
    #table_joueurs.truncate()

    def __init__(self, view):
        self.view = view
        self.joueurs: List[Joueur] = []



    def get_joueur(self):

        joueur_info = self.view.prompt_joueur()
        joueur = Joueur(joueur_info[0], joueur_info[1], joueur_info[2],
                        joueur_info[3], joueur_info[4])
        serialized_joueur = {
            'nom': joueur.nom,
            'prenom': joueur.prenom,
            'date_de_naissance': joueur.date_de_naissance,
            'sexe': joueur.sexe,
            'classement': joueur.classement
                           }
        self.table_joueurs.insert(serialized_joueur)

        pprint.pprint(self.table_joueurs.all())
        return joueur

    def afficher_joueurs(self, joueurs_tournoi):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        User = Query()
        print("Liste des Joueurs")
        for joueur in table_joueurs:
            if str(joueur.doc_id) not in joueurs_tournoi:
                results = str(joueur.doc_id) + " : " + joueur["prenom"] + " " + \
                          joueur["nom"] + " (" + joueur["classement"] + ")"
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

    def creer_tournoi(self):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        User = Query()
        tournoi_info = self.view.prompt_tournoi()
        joueurs_tournoi = []
        i = 1
        while i < 9:
            self.afficher_joueurs(joueurs_tournoi)
            indice = self.view.prompt_joueur_tournoi(i)
            if self.verifier_indice(indice) == True and indice not in joueurs_tournoi:
                i += 1
                serialized_joueur = self.recuperer_joueur(indice)
                joueur = Joueur(
                    serialized_joueur['nom'],
                    serialized_joueur['prenom'],
                    serialized_joueur['date_de_naissance'],
                    serialized_joueur['sexe'],
                    serialized_joueur['classement']
                              )
                self.joueurs.append(joueur)
                joueurs_tournoi.append(indice)







        tournoi = Tournoi(tournoi_info[0], tournoi_info[1], tournoi_info[2], tournoi_info[3],
                          tournoi_info[4], tournoi_info[5], tournoi_info[6], self.joueurs, flag="En Cours"
                          )

        self.table_tournois.insert({'nom_tournoi': tournoi.nom_tournoi, 'lieu': tournoi.lieu, 'date_debut': tournoi.date_debut,
                                    'date_fin': tournoi.date_fin, 'nombre_tours': tournoi.nombre_tours,
                                    'controle_temps': tournoi.controle_du_temps, 'description': tournoi.description,
                                    'joueurs': joueurs_tournoi, 'flag': tournoi.flag,
                                   })

        self.generation_paires(1, tournoi)

    def recuperer_joueur(self, indice):
        for joueur in self.table_joueurs:
            if str(joueur.doc_id) == indice:
                return joueur



    def verifier_indice(self, indice):
        db = TinyDB('db.json')
        table_joueurs = db.table("joueurs")
        User = Query()
        for joueur in table_joueurs:
            if str(joueur.doc_id) == indice:
                return True

    def afficher_liste_tournois(self):
        db = TinyDB('db.json')
        table_tournois = db.table("tournois")
        User = Query()
        print("Liste Des Tournois")

        for tournoi in table_tournois:
            results = str(tournoi.doc_id) + " : " + tournoi["nom_tournoi"] + " " + \
                      tournoi["lieu"] + " (" + tournoi["date_debut"] + ")"
            print(results)


    def generation_paires(self, num_tour, tournoi: Tournoi):
         if num_tour == 1:
            # creer tour
            # tour = creer un tour
            # nom_tour = "Round1"
            # heure debut horodatage
            # heure fin vide
            # liste de match vide
            ranked_joueurs = sorted(tournoi.joueurs, key=lambda x: x.classement, reverse=True)

            '''
            match1 = Match("match1", ranked_joueurs[0], point_player0, ranked_joueurs[4], point_player4)
            db.insert({"round": "round1", "match": "match1",
                       "player1": players[0].first_name,
                       "score1": point_player0,
                       "player2": players[4].first_name,
                       "score2": point_player4
                       })

            match2 = Match("match2", ranked_joueurs[1], point_player1, ranked_joueurs[5], point_player5)
            db.insert({"round": "round1", "match": "match2",
                       "player1": players[1].first_name,
                       "score1": point_player1,
                       "player2": players[5].first_name,
                       "score2": point_player5
                       })

            match3 = Match("match3", ranked_joueurs[2], point_player2, ranked_joueurs[6], point_player6)
            db.insert({"round": "round1", "match": "match3",
                       "player1": players[2].first_name,
                       "score1": point_player2,
                       "player2": players[6].first_name,
                       "score2": point_player6
                       })

            match4 = Match("match4", ranked_joueurs[3], point_player3, ranked_joueurs[7], point_player7)
            db.insert({"round": "round1", "match": "match4",
                       "player1": players[3].first_name,
                       "score1": point_player3,
                       "player2": players[7].first_name,
                       "score2": point_player7
                       })

            # print(players[4].first_name)

            round1_matchs = [match1, match2, match3, match4]
            round1 = Round(round_matchs=round1_matchs, round_name="Round1",
                           start_date=view.round1_start_date, start_time=view.round1_start_time,
                           end_date=view.round1_end_date, end_time=view.round1_end_time
                           )'''

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
            self.creer_tournoi()
        elif index == str(2):
            self.afficher_liste_tournois()
        elif index == str(3):
            ids = input("entrez l'id")
            self.recuperer_joueur(ids)
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

