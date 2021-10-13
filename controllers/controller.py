from datetime import datetime
from tinydb import TinyDB
from typing import List
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round


class Controller:

    def __init__(self, view):
        self.view = view
        self.ranked_players: List[Player] = []
        self.players: List[Player] = []
        db = TinyDB('db.json')
        self.table_players = db.table("players")
        self.table_tournaments = db.table("tournaments")
        self.tournament: Tournament
        self.round_of_input = 0
        # self.table_players.truncate()
        # self.table_tournaments.truncate()

    def test(self):
        self.has_first_round_started(1)

    def add_new_empty_round_to_tournament(self, tournament_id):
        serialized_new_round = Round.serialize_round(Round.create_empty_new_round_in_tournament(tournament_id))
        Round.append_round_in_table(tournament_id, serialized_new_round)

    def get_eight_players_ids(self):
        players_ids = []
        players_in_tournament = []
        i = 1
        while i < 9:
            self.view.display_players_not_in_tournament(players_in_tournament)
            player_id = self.view.prompt_add_player_id_to_tournament(i)
            if Player.check_player_id(player_id) == True and player_id not in players_in_tournament:
                i += 1
                players_ids.append(player_id)
                players_in_tournament.append(player_id)
        return players_ids

    def get_player_info(self):
        player_info = self.view.prompt_player_info()
        return player_info

    def create_player(self):
        player_info = self.get_player_info()
        Player.get_new_player(player_info).save()

    def update_player_ranking(self):
        self.view.display_players([])
        player_id = self.view.prompt_player_id_for_update()
        new_ranking = self.view.prompt_input_new_ranking()
        for player in self.table_players:
            if str(player.doc_id) == player_id:
                self.table_players.update({"ranking": new_ranking}, doc_ids=[player.doc_id])
                self.view.prompt_modification_success()

    """Tournament"""
    def create_new_tournament(self):
        DB_HAS_AT_LEAST_8_PLAYERS = Player.number_of_players_in_db() >= 8
        if DB_HAS_AT_LEAST_8_PLAYERS == True:
            serialized_new_tournament = self.view.prompt_new_tournament()
            players_ids = self.get_eight_players_ids()
            serialized_new_tournament['players'] = players_ids
            serialized_new_tournament['flag'] = "Tournament In Progress"
            serialized_new_tournament['rounds'] = []
            self.table_tournaments.insert(serialized_new_tournament)
        else:
            self.view.prompt_alert_not_enough_players()
            self.display_sub_menu("1")

    def translate_results(self, entry):
        score1 = 0
        score2 = 0
        if entry == str(1):
            score1 = 1
            score2 = 0
        elif entry == str(2):
            score1 = 0
            score2 = 1
        elif entry == "x":
            score1 = 0.5
            score2 = 0.5

        return [score1, score2]

    def get_round_of_input(self, tournament_id):
        tournament_in_table = self.table_tournaments.get(doc_id=int(tournament_id))
        last_round_index = Round.last_round_index_in_table(tournament_id)
        if last_round_index == 0:
            '''create first round'''

        elif last_round_index > 1 and last_round_index <= 4 :
            '''input pending round'''
            self.round_of_input = last_round_index
        elif last_round_index > 1 and tournament_in_table['rounds'][last_round_index]['flag'] == "Round Finished" and last_round_index < 4:
            '''create new round'''
            new_round = Round.create_empty_new_round_in_tournament(tournament_id)
            Round.append_round_in_table(tournament_id, new_round)
            self.round_of_input = last_round_index + 2
        elif last_round_index == 4:
            print("The Tournament is Finished")
        return self.round_of_input

    def has_first_round_started(self, tournament_id):
        tournament_in_table = self.table_tournaments.get(doc_id=int(tournament_id))
        rounds_in_table = tournament_in_table['rounds']
        latest_round = len(rounds_in_table)
        if latest_round > 0:
            return True
        elif latest_round == 0:
            return False


    def is_last_round_finished(self, tournament_id):
        """function returns 1 if a round needs to be created and 0 if the last round needs to be created"""
        tournament_in_table = self.table_tournaments.get(doc_id=int(tournament_id))
        last_round = self.what_is_latest_round(tournament_id)
        if last_round == 0:
            return False
        elif last_round > 0:
            if tournament_in_table['rounds'][last_round - 1]['flag'] == "Round Finished":
                return True
            elif tournament_in_table['rounds'][last_round - 1]['flag'] == "Round In Progress":
                return False


    def what_is_latest_round(self, tournament_id):
        tournament_in_table = self.table_tournaments.get(doc_id=int(tournament_id))
        rounds_in_table = tournament_in_table['rounds']
        latest_round = len(rounds_in_table)
        return latest_round

    def do_i_need_a_new_round(self, tournament_id):
        print("has_first_round_started(tournament_id)")
        print(self.has_first_round_started(tournament_id))
        print("self.is_last_round_finished(tournament_id)")
        print(self.is_last_round_finished(tournament_id))
        if self.has_first_round_started(tournament_id) == False or self.is_last_round_finished(tournament_id):
            return True
        else:
            return False

    def is_tournament_over(self, tournament_id):
        MAX_ROUNDS = 4
        if self.what_is_latest_round(tournament_id) == MAX_ROUNDS and self.is_last_round_finished(tournament_id):
            return True
        else:
            return False


    def input_results(self):
        MAX_ROUNDS = 4
        self.view.display_all_tournaments()
        tournament_id = self.view.prompt_choose_tournament_id()
        self.view.display_rounds_from_tournament_id(tournament_id)
        print("what_is_latest_round")
        print(self.what_is_latest_round(tournament_id))
        print("is_tournament_over(tournament_id)")
        print(self.is_tournament_over(tournament_id))
        print("do_i_need_a_new_round(tournament_id)")
        print(self.do_i_need_a_new_round(tournament_id))

        if self.is_tournament_over(tournament_id) == False:
            if self.do_i_need_a_new_round(tournament_id):
                print("do_i_need_a_new_round")
                new_round = Round.create_empty_new_round_in_tournament(tournament_id)
                Round.append_round_in_table(tournament_id, new_round)

            round_number = self.what_is_latest_round(tournament_id)
            print("round number")
            print(round_number)

            if round_number == 1:
                self.generate_first_round(tournament_id, round_number)
            elif 1 < round_number <= MAX_ROUNDS:
                self.generate_other_round(tournament_id, round_number)
            else:
                print("ROUND ERROR")
        else:
            self.view.prompt_alert_round_input()
            self.display_sub_menu("2")



    def aggregate_player_score(self, player_id, tournament_id):
        player_score = 0.0
        for tournament_in_table in self.table_tournaments:
            if str(tournament_id) == str(tournament_in_table.doc_id):
                rounds_in_table = tournament_in_table['rounds']
                for round_in_table in rounds_in_table:
                    matchs_in_table = round_in_table['round_matchs']
                    for match_in_table in matchs_in_table:
                        if str(match_in_table['result'][0][0]) == player_id:
                            player_score += match_in_table['result'][0][1]
                        if match_in_table['result'][1][0] == player_id:
                            player_score += match_in_table['result'][0][1]
        return player_score

    def has_player_played_against(self, player_id, opponent_id, tournament_id):
        tournament = self.table_tournaments.get(doc_id=int(tournament_id))
        rounds_in_table = tournament['rounds']
        matchs = []
        response = False
        for round_in_table in rounds_in_table:
            tournament_matchs = round_in_table['round_matchs']
            for match_in_table in tournament_matchs:
                matchs.append(match_in_table)

        for match in matchs:
            if str(player_id) == str(match['result'][0][0]) or str(player_id) == str(match['result'][1][0]):
                if str(opponent_id) == match['result'][1][0] or str(player_id) == str(match['result'][1][0]):
                    response = True

                return response

    def timestamp(self):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return timestamp

    def generate_first_round(self, tournament_id, round_number):
        players = Player.get_players_from_tournament_id(tournament_id)
        start_round_timestamp = self.timestamp()
        self.round_matchs = self.generate_first_round_matchs(players)
        end_round_timestamp = self.timestamp()
        # Round Creation
        round_name = "Round " + str(round_number)
        round = Round(str(round_number), round_name, start_round_timestamp, end_round_timestamp, self.round_matchs,
                      "Round Finished")

        print("round_matchs")
        print(self.round_matchs)
        Round.update_round_in_table(tournament_id, round)

    def generate_first_round_matchs(self, players):
        self.ranked_players = sorted(players, key=lambda x: x.ranking, reverse=True)
        number_of_players = len(self.ranked_players)
        i = 0
        self.round_matchs = []
        while 2 * i < number_of_players:
            index1 = i
            index2 = (i + int(number_of_players / 2))
            result = self.view.prompt_input_match_result(self.ranked_players[index1], self.ranked_players[index2])
            player_white_result = [self.ranked_players[index1], self.translate_results(result)[0]]
            player_black_result = [self.ranked_players[index2], self.translate_results(result)[1]]
            match_result = (player_white_result, player_black_result)
            match = Match(match_result)
            self.round_matchs.append(match)
            i += 1
        return self.round_matchs

    def generate_other_round(self, tournament_id, round_number):

        players = Player.get_players_from_tournament_id(tournament_id)
        start_round_timestamp = self.timestamp()
        self.round_matchs = self.generate_other_round_matchs(players)
        end_round_timestamp = self.timestamp()
        print(self.round_matchs)

        # Round Creation
        round_name = "Round " + str(round_number)
        round = Round(str(round_number), round_name, start_round_timestamp, end_round_timestamp, self.round_matchs,
                      "Round Finished")
        # Finish Here
        print("update round")
        Round.update_round_in_table(tournament_id, round)

    def generate_other_round_matchs(self, players):
        self.ranked_players = sorted(players, key=lambda x: (x.tournament_score, x.ranking), reverse=True)
        number_of_players = len(self.ranked_players)
        i = 0
        self.round_matchs = []
        while i < number_of_players:
            index1 = i
            index2 = (i + 1)
            result = self.view.prompt_input_match_result(self.ranked_players[index1], self.ranked_players[index2])
            player_white_result = [self.ranked_players[index1], self.translate_results(result)[0]]
            player_black_result = [self.ranked_players[index2], self.translate_results(result)[1]]
            match_result = (player_white_result, player_black_result)
            match = Match(match_result)
            self.round_matchs.append(match)
            i += 2

    def generate_pairs(self, round_number, tournament_id):
        '''pour limiter le code mettre get_joueurs dans get_tournoi'''
        self.tournament = Tournament.get_tournament_from_id(tournament_id)

        if str(round_number) == "1":
            start_round_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.ranked_players = sorted(self.tournament.players, key=lambda x: x.ranking, reverse=True)
            number_of_players = len(self.ranked_players)
            i = 0
            self.round_matchs = []
            while 2 * i < number_of_players:
                # Generation de la liste des matchs dans round_matchs
                index1 = i
                index2 = (i + int(number_of_players / 2))
                result = self.view.prompt_input_match_result(self.ranked_players[index1], self.ranked_players[index2])
                player_white_result = [self.ranked_players[index1], self.translate_results(result)[0]]
                player_black_result = [self.ranked_players[index2], self.translate_results(result)[1]]
                match_result = (player_white_result, player_black_result)
                match = Match(match_result)
                self.round_matchs.append(match)
                i += 1

            # Enregistrement Objet Tour
            round_name = "Round " + str(round_number)
            end_round_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            round = Round(str(round_number), round_name, start_round_timestamp, end_round_timestamp, self.round_matchs,
                          "Round Finished")

            # Serialisation du Tour
            serialized_rounds = []
            serialized_round = round.serialize_round()
            serialized_rounds.append(serialized_round)
            # Mise à Jour de Tour dans le Tournoi
            for tournament_in_table in self.table_tournaments:
                if str(tournament_in_table.doc_id) == str(tournament_id):
                    self.table_tournaments.update({"rounds": serialized_rounds},
                                               doc_ids=[tournament_in_table.doc_id])

            # Generation du Tour Suivant
            next_round_number = str(int(round_number) + 1)
            next_round_name = "Round " + str(next_round_number)
            next_round = Round(next_round_number, next_round_name, None, None, [], "In Progress")
            serialized_next_round = next_round.serialize_round()
            serialized_rounds = Round.get_rounds_from_tournament_id(tournament_id)
            serialized_rounds.append(serialized_next_round)
            # Mise à Jour de Tour dans le Tournoi
            for tournament_in_table in self.table_tournaments:
                if str(tournament_in_table.doc_id) == str(tournament_id):
                    self.table_tournaments.update({"rounds": serialized_rounds}, doc_ids=[tournament_in_table.doc_id])

        if int(round_number) > 1 and int(round_number) <= 4:
            start_round_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Ecriture des score cumules
            for player in self.tournament.players:
                player_id = player.get_player_id()
                player.tournament_score = self.aggregate_player_score(player_id, tournament_id)

            self.ranked_players = sorted(self.tournament.players, key=lambda x: (x.tournament_score, x.ranking), reverse=True)
            number_of_players = len(self.ranked_players)
            i = 0
            self.round_matchs = []
            while i < number_of_players:
                # Generation de la liste des matchs dans round_matchs
                index1 = i
                index2 = (i + 1)

                result = self.view.prompt_input_match_result(self.ranked_players[index1], self.ranked_players[index2])

                player_white_result = [self.ranked_players[index1], self.translate_results(result)[0]]
                player_black_result = [self.ranked_players[index2], self.translate_results(result)[1]]
                match_result = (player_white_result, player_black_result)
                match = Match(match_result)
                self.round_matchs.append(match)
                i += 2

            # Enregistrement Objet Tour
            round_name = "Round " + str(round_number)
            end_round_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            round = Round(str(round_number), round_name, start_round_timestamp, end_round_timestamp, self.round_matchs,
                        "Finished")

            # Serialisation du Tour
            serialized_rounds = Round.get_rounds_from_tournament_id(tournament_id)
            serialized_rounds.pop()
            serialized_round = round.serialize_round()
            serialized_rounds.append(serialized_round)

            # Mise à Jour de Tour dans le Tournoi
            for tournament_in_table in self.table_tournaments:
                if str(tournament_in_table.doc_id) == str(tournament_id):
                    self.table_tournaments.update({"rounds": serialized_rounds},
                                               doc_ids=[tournament_in_table.doc_id])

            # Generation du Tour Suivant
            if int(round_number) < int(self.tournament.number_of_rounds):
                next_round_number = str(int(round_number) + 1)
                next_round_name = "Round " + str(next_round_number)
                next_round = Round(next_round_number, next_round_name, None, None, [], "In Progress")
                serialized_next_round = next_round.serialize_round()
                serialized_rounds = Round.get_rounds_from_tournament_id(tournament_id)
                serialized_rounds.append(serialized_next_round)

                # Mise à Jour de Tour dans le Tournoi
                for tournament_in_table in self.table_tournaments:
                    if str(tournament_in_table.doc_id) == str(tournament_id):
                        self.table_tournaments.update({"rounds": serialized_rounds},
                                                      doc_ids=[tournament_in_table.doc_id])
            # Flag Tournoi Termine
            if int(round_number) == int(self.tournament.number_of_rounds):
                # Flag Tournoi Termine
                for tournament_in_table in self.table_tournaments:
                    if str(tournament_in_table.doc_id) == str(tournament_id):
                        self.table_tournaments.update({'flag': 'Finished'}, doc_ids=[tournament_in_table.doc_id])



    """Menu Functions"""

    def run(self):
        self.display_main_menu()

    def display_main_menu(self):
        index = self.view.display_menu()
        self.display_sub_menu(index)

    def display_sub_menu(self, index):
        if index == str(1):
            index2 = self.view.display_menu_players()
            self.display_sub_menu_players(index2)
        elif index == str(2):
            index2 = self.view.display_menu_tournaments()
            self.display_sub_menu_tournaments(index2)
        elif index == str(3):
            index2 = self.view.display_menu_reports()
            self.display_sub_menu_reports(index2)
        elif index == str(4):
            self.display_main_menu()
        elif str(index).upper() == "Q":
            exit()

    def display_sub_menu_players(self, index):
        if index == str(1):
            self.create_player()
        elif index == str(2):
            self.update_player_ranking()
        elif index == str(3):
            self.view.display_players([])
        elif index == str(4):
            self.display_main_menu()
        elif index == str(5):
            self.test()
        elif str(index).upper() == "Q":
            exit()
        self.display_sub_menu("1")

    def display_sub_menu_tournaments(self, index):
        if index == str(1):
            self.create_new_tournament()
        elif index == str(2):
            self.view.display_all_tournaments()
        elif index == str(3):
            self.input_results()
            self.display_sub_menu("2")
        elif index == str(4):
            self.display_main_menu()
        elif str(index).upper() == "Q":
            exit()
        self.display_sub_menu("2")

    def display_sub_menu_reports(self, index):
        if index == str(1):
            self.view.display_players_alphabetical()
        elif index == str(2):
            self.view.display_players_by_ranking()
        elif index == str(3):
            self.view.display_tournament_players_alphabetical()
        elif index == str(4):
            self.view.display_tournaments_players_by_ranking()
        elif index == str(5):
            self.view.display_all_tournaments()
        elif index == str(6):
            self.view.display_all_tournaments()
            tournament_id = self.view.prompt_choose_tournament_id()
            '''self.view.display_rounds_from_tournament_id(tournament_id)'''
            tournament_id = self.view.display_tournament_rounds(tournament_id)
        elif index == str(7):
            self.view.display_tournament_matchs()
        elif index == str(8):
            self.display_main_menu()
        elif str(index).upper() == "Q":
            exit()
        self.display_sub_menu("3")
