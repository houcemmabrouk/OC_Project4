from datetime import datetime
from tinydb import TinyDB, Query, where
import pprint
from typing import List
from models.joueur import Joueur
from models.tournoi import Tournoi
from models.match import Match
from models.tour import Tour

class Controller:


    db = TinyDB('db.json')

    table_joueurs = db.table("joueurs")
    table_tournois = db.table("tournois")


    def __init__(self, view):
        self.view = view
        self.joueurs: List[Joueur] = []
        self.matchs_tour: List[Match] = []
        self.tours_tournoi: List[Tour] = []
        self.ranked_joueurs: List[Joueur] = []
        self.tours: List[Match] = []
        db = TinyDB('db.json')
        self.table_joueurs = db.table("joueurs")
        self.table_tournois = db.table("tournois")



    def effacer_tous_joueurs(self):
        self.table_tournois.truncate()

    def effacer_tous_tournois(self):
        self.table_joueurs.truncate()

    def set_joueur(self):

        joueur_info = self.view.prompt_joueur()
        joueur = Joueur(joueur_info[0], joueur_info[1], joueur_info[2],
                        joueur_info[3], joueur_info[4], 0)
        serialized_joueur = {
            'nom': joueur.nom,
            'prenom': joueur.prenom,
            'date_de_naissance': joueur.date_de_naissance,
            'sexe': joueur.sexe,
            'classement': joueur.classement,
            'score_tournoi': joueur.score_tournoi
                           }
        self.table_joueurs.insert(serialized_joueur)
        pprint.pprint(self.table_joueurs.all())
        return joueur

    def get_joueurs_ids(self, joueurs):
        joueurs_ids = []
        for joueur in joueurs:
            joueur_id = self.get_joueur_id(joueur)
            joueurs_ids.append(joueur_id)
        return joueurs_ids

    def serialize_joueur(self, joueur):
        serialized_joueur = {
                            'nom': joueur.nom,
                            'prenom': joueur.prenom,
                            'date_de_naissance': joueur.date_de_naissance,
                            'sexe': joueur.sexe,
                            'classement': joueur.classement,
                            'score_tournoi': joueur.score_tournoi
                            }
        return serialized_joueur

    def deserialize_joueur(self, serialized_joueur):
        joueur = Joueur(
                        nom=serialized_joueur['nom'],
                        prenom=serialized_joueur['prenom'],
                        date_de_naissance=serialized_joueur['date_de_naissance'],
                        sexe=serialized_joueur['sexe'],
                        classement=serialized_joueur['classement'],
                        score_tournoi=serialized_joueur['score_tournoi']
                        )
        return joueur

    def serialize_match(self, match):
        joueur_blanc_id = self.get_joueur_id(match.resultat[0][0])
        score_blanc = match.resultat[0][1]
        joueur_noir_id = self.get_joueur_id(match.resultat[1][0])
        score_noir = match.resultat[1][1]
        match_resultat = ([joueur_blanc_id, score_blanc], [joueur_noir_id, score_noir])
        serialized_match = {'resultat': match_resultat}
        return serialized_match

    def deserialize_match(self, serialized_match):
        joueur_blanc = self.get_joueur(serialized_match[0][0])
        score_blanc = serialized_match[0][1]
        joueur_noir = self.get_joueur(serialized_match[1][0])
        score_noir = serialized_match[1][1]
        resultat_match = ([joueur_blanc, score_blanc], [joueur_noir, score_noir])
        match = Match(resultat=resultat_match)
        return match

    def serialize_tour(self, tour):
        tour_matchs = []
        for match in tour.tour_matchs:
            tour_match = self.serialize_match(match)
            tour_matchs.append(tour_match)

        serialized_tour = {
                            'nom_tour': tour.nom_tour,
                            'date_debut': tour.date_debut,
                            'date_fin': tour.date_fin,
                            'tour_matchs': tour_matchs,
                            'id_tournoi': tour.id_tournoi,
                            }
        return serialized_tour

    def deserialize_tour(self, serialized_tour):
        tour_matchs = []
        for match in serialized_tour['tour_matchs']:
            deserialized_match = self.deserialize_match(match)
            tour_matchs.append(deserialized_match)

        tour = Tour(
                    nom_tour=serialized_tour['nom'],
                    date_debut=serialized_tour['date_debut'],
                    date_fin=serialized_tour['date_fin'],
                    tour_matchs=serialized_tour['tour_matchs'],
                    flag=serialized_tour['flag'],
                    id_tournoi=serialized_tour['id_tournoi']
                    )
        return tour

    def serialize_tournoi(self, tournoi):
        serialized_tournoi = {
                            'nom_tournoi': tournoi.nom_tournoi,
                            'lieu': tournoi.lieu,
                            'date_debut': tournoi.date_debut,
                            'date_fin': tournoi.date_fin,
                            'nombre_tours': tournoi.nombre_tours,
                            'joueurs': self.get_joueurs_ids(tournoi.joueurs),
                            'controle_du_temps': tournoi.controle_du_temps,
                            'description': tournoi.description,
                            'tours': tournoi.tours,
                            'flag': tournoi.flag
                            }
        return serialized_tournoi

    def get_joueur_id(self, joueur):
        User = Query()
        serialized_joueur = self.serialize_joueur(joueur)
        print(serialized_joueur['nom'])
        documents = self.table_joueurs.search(User.nom == str(serialized_joueur['nom']))
        print(documents)
        id_joueur = None
        for document in documents:
            id_joueur = document.doc_id
        return id_joueur

    def get_joueurs(self, ids_joueurs):
        joueurs = []
        for id_joueur in ids_joueurs:
            for joueur in self.table_joueurs:
                if str(id_joueur) == str(joueur.doc_id):
                    joueur = Joueur(
                                    joueur['nom'],
                                    joueur['prenom'],
                                    joueur['date_de_naissance'],
                                    joueur['sexe'],
                                    joueur['classement'],
                                    joueur['score_tournoi']
                                    )
                    joueurs.append(joueur)
        return joueurs

    def get_joueur(self, id_joueur):
        for joueur_in_table in self.table_joueurs:
            if str(id_joueur) == str(joueur_in_table.doc_id):
                joueur = Joueur(
                                joueur_in_table['nom'],
                                joueur_in_table['prenom'],
                                joueur_in_table['date_de_naissance'],
                                joueur_in_table['sexe'],
                                joueur_in_table['classement'],
                                joueur_in_table['score_tournoi']
                                )

        return joueur
    # a mettre dans la vue
    # sauf ecriture base de données
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
        self.afficher_joueurs([])
        joueur_id = self.view.prompt_get_id()
        nouveau_classement = self.view.prompt_get_nouveau_classement()

        for joueur in table_joueurs:
            if str(joueur.doc_id) == joueur_id:
                table_joueurs.update({"classement": nouveau_classement}, doc_ids=[joueur.doc_id])
                # a gerer par la vue
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
                    serialized_joueur['classement'],
                    serialized_joueur['score_tournoi']
                              )
                self.joueurs.append(joueur)
                joueurs_tournoi.append(indice)


        '''Creation du tournoi'''
        tournoi = Tournoi(tournoi_info[0], tournoi_info[1], tournoi_info[2], tournoi_info[3],
                          tournoi_info[4], tournoi_info[5], tournoi_info[6], self.joueurs, self.tours, flag="En Cours"
                          )
        serialized_tournoi = {
                            'nom_tournoi': tournoi.nom_tournoi,
                            'lieu': tournoi.lieu,
                            'date_debut': tournoi.date_debut,
                            'date_fin': tournoi.date_fin,
                            'nombre_tours': tournoi.nombre_tours,
                            'joueurs': joueurs_tournoi,
                            'controle_du_temps': tournoi.controle_du_temps,
                            'description': tournoi.description,
                            'tours': self.tours,
                            'flag': tournoi.flag
                            }
        self.table_tournois.insert(serialized_tournoi)
        pprint.pprint(self.table_tournois.all())
        '''Creation du premier Tour'''
        self.generation_paires(1, tournoi)

    def get_tournoi(self, id_tournoi):
        for tournoi_in_table in self.table_tournois:
            if str(id_tournoi) == str(tournoi_in_table.doc_id):
                tournoi = Tournoi(nom_tournoi=tournoi_in_table['nom_tournoi'],
                                  lieu=tournoi_in_table['lieu'],
                                  date_debut=tournoi_in_table['date_debut'],
                                  date_fin=tournoi_in_table['date_fin'],
                                  nombre_tours=tournoi_in_table['nombre_tours'],
                                  controle_du_temps=tournoi_in_table['controle_du_temps'],
                                  description=tournoi_in_table['description'],
                                  joueurs=tournoi_in_table['joueurs'],
                                  tours=tournoi_in_table['tours'],
                                  flag=tournoi_in_table['flag']
                                  )
                return tournoi

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
        # a gerer par la vue
        print("Liste Des Tournois")

        for tournoi in table_tournois:
            results = str(tournoi.doc_id) + " : " + tournoi["nom_tournoi"] + " " + \
                      tournoi["lieu"] + " (" + tournoi["date_debut"] + ")"
            print(results)

    def generation_paires(self, num_tour, id_tournoi):


        tournoi = self.get_tournoi(int(id_tournoi))
        tournoi.joueurs = self.get_joueurs(tournoi.joueurs)
        print(tournoi.joueurs)
        print(self.get_joueurs(tournoi.joueurs))
        if num_tour == 1:
            self.ranked_joueurs = sorted(tournoi.joueurs, key=lambda x: x.classement, reverse=True)
            nb_joueurs = len(self.ranked_joueurs)

            horodatage_debut_tour = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


            i = 0
            while 2*i < nb_joueurs:
                score1 = 0
                score2 = 0
                index1 = i
                index2 = (i + int(nb_joueurs/2))
                resultat = self.view.prompt_resultat_match(self.ranked_joueurs[index1],
                                                           self.ranked_joueurs[index2])

                if resultat == str(1):
                    score1 = 1
                    score2 = 0
                elif resultat == str(2):
                    score1 = 0
                    score2 = 1
                elif resultat == "x":
                    score1 = 0.5
                    score2 = 0.5

                joueur_blanc = [self.ranked_joueurs[index1], score1]
                joueur_noir = [self.ranked_joueurs[index2], score2]

                '''reprendre ici
                self.ranked_joueurs[index1].'''



                #horodatage_match = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                match = Match(resultat=(joueur_blanc, joueur_noir))
                self.matchs_tour.append(match)
                i += 1

            for match in self.matchs_tour:
                for joueur in tournoi.joueurs:
                    if joueur == match.resultat[0][0]:
                        joueur.score_tournoi = match.resultat[0][1]
            for match in self.matchs_tour:
                for joueur in tournoi.joueurs:
                    if joueur == match.resultat[1][0]:
                        joueur.score_tournoi = match.resultat[1][1]

            for joueur in tournoi.joueurs:
                print(joueur.score_tournoi)

            nom_tour ="tour " + str(num_tour)

            '''enregistrement tour'''
            tour = Tour(nom_tour, horodatage_debut_tour, None, self.matchs_tour, "Terminé", id_tournoi)
            tours_tournoi = []
            tours_tournoi.append(tour)
            tournoi.tours = tours_tournoi




            serialized_tour = {
                                'nom_tour': tour.nom_tour,
                                'date_debut': tour.date_debut,
                                'date_fin': tour.date_fin,
                                'tour_matchs': tour.tour_matchs,
                                'id_tournoi': tour.id_tournoi,
                                }




            for tournoi_in_table in self.table_tournois:
                if str(tournoi_in_table.doc_id) == str(id_tournoi):
                    self.table_tournois.update({"tours": tours_tournoi},
                                               doc_ids=[tournoi_in_table.doc_id])


            for match in tour.tour_matchs:
                print(match.resultat[0] + match.resultat[1])


        elif num_tour > 1 and num_tour <= int(tournoi.nombre_tours):
            ranked_joueurs = sorted(tournoi.joueurs, key=lambda x: (x.score_tournoi, x.ranking), reverse=True)

            nb_joueurs = len(ranked_joueurs)

            horodatage_debut_tour = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            i = 0
            while 2 * i < nb_joueurs:
                score1 = 0
                score2 = 0
                index1 = i
                index2 = (i + 1)
                resultat = self.view.prompt_resultat_match(ranked_joueurs[index1],
                                                           ranked_joueurs[index2])
                print(resultat)
                if resultat == str(1):
                    score1 = 1
                    score2 = 0
                elif resultat == str(2):
                    score1 = 0
                    score2 = 1
                elif resultat == "x":
                    score1 = 0.5
                    score2 = 0.5

                joueur_blanc = [ranked_joueurs[index1], score1]
                joueur_noir = [ranked_joueurs[index2], score2]
                horodatage_match = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                match = Match(resultat=(joueur_blanc, joueur_noir))

                print(match.resultat)
                print(match.horodatage)

                self.matchs_tour.append(match)

                i += 1
                print(i)

            nom_tour = "tour" + str(num_tour)

            tour = Tour(nom_tour, horodatage_debut_tour, None, self.matchs_tour, "En cours", id_tournoi)
            self.tours_tournoi.append(tour)

    def saisir_resultat(self):
        db = TinyDB('db.json')
        table_tournois = db.table("tournois")
        User = Query()
        self.afficher_liste_tournois()
        indice_tournoi = self.view.prompt_choisir_tournoi()
        i = 0

        for tournoi in table_tournois:
            if str(tournoi.doc_id) == indice_tournoi:
                tournoi = self.get_tournoi(indice_tournoi)
                i += 1
                dernier_tour = len(tournoi.tours) + 1



        id_tournoi = indice_tournoi
        num_tour = dernier_tour
        self.generation_paires(num_tour, id_tournoi)

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
            self.set_joueur()
        elif index == str(2):
            self.update_joueur_classement()
        elif index == str(3):
            self.afficher_joueurs([])
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
            self.saisir_resultat()
            self.afficher_sous_menu("2")
        elif index == str(4):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()
        self.afficher_sous_menu("2")

    def afficher_sous_menu_match(self, index):
        if index == str(1):
            self.get_joueurs([1, 2, 3, 4])
        elif index == str(2):
            self.afficher_menu_principal()
        elif str(index).upper() == "Q":
            exit()

