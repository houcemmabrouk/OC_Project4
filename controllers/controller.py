from datetime import datetime
from tinydb import TinyDB
from typing import List
from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament


class Controller:

    def __init__(self, view):
        self.view = view
        self.ranked_players: List[Player] = []
        self.players: List[Player] = []
        db = TinyDB('db.json')
        self.table_players = db.table("players")
        self.table_tournaments = db.table("tournaments")
        # self.table_players.truncate()
        # self.table_tournaments.truncate()

    """Player"""

    def get_player_info(self):
        player_info = self.view.prompt_player_info()
        return player_info

    def create_player(self):
        player_info = self.get_player_info()
        Player.get_new_player(player_info).save()

    def update_player_ranking(self):
        if not Tournament.is_table_tournaments_empty():
            self.view.display_players([])
            player_id = self.view.prompt_player_id_for_update()
            new_ranking = self.view.prompt_input_new_ranking()
            for player in self.table_players:
                if str(player.doc_id) == str(player_id):
                    self.table_players.update({"ranking": str(new_ranking)}, doc_ids=[player.doc_id])
                    self.view.prompt_modification_success()
        else:
            self.view.prompt_alert_table_player_emty()
            self.display_sub_menu("1")

    """Tournament"""

    def create_new_tournament(self):
        DB_HAS_AT_LEAST_8_PLAYERS = Player.number_of_players_in_db() >= 8
        if DB_HAS_AT_LEAST_8_PLAYERS:
            serialized_new_tournament = self.view.prompt_new_tournament()
            players_ids = self.get_eight_players_ids()
            serialized_new_tournament['players'] = players_ids
            serialized_new_tournament['flag'] = "Tournament In Progress"
            serialized_new_tournament['rounds'] = []
            self.table_tournaments.insert(serialized_new_tournament)
        else:
            self.view.prompt_alert_not_enough_players()
            self.display_sub_menu("1")

    def get_eight_players_ids(self):
        players_ids = []
        players_in_tournament = []
        i = 1
        while i < 9:
            self.view.display_players(players_in_tournament)
            player_id = self.view.prompt_add_player_id_to_tournament(i)
            if Player.check_player_id(player_id) and player_id not in players_in_tournament:
                i += 1
                players_ids.append(player_id)
                players_in_tournament.append(player_id)
        return players_ids

    def add_new_empty_round_to_tournament(self, tournament_id):
        serialized_new_round = Round.serialize_round(Round.create_empty_new_round_in_tournament(tournament_id))
        Round.append_round_in_table(tournament_id, serialized_new_round)

    def has_first_round_started(self, tournament_id):
        tournament_in_table = self.table_tournaments.get(doc_id=int(tournament_id))
        rounds_in_table = tournament_in_table['rounds']
        return len(rounds_in_table) > 0

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
        if self.has_first_round_started(tournament_id) is False or self.is_last_round_finished(tournament_id):
            return True
        else:
            return False

    def is_tournament_over(self, tournament_id):
        MAX_ROUNDS = 4
        if self.what_is_latest_round(tournament_id) == MAX_ROUNDS and self.is_last_round_finished(tournament_id):
            return True
        else:
            return False

    def generate_first_round(self, tournament_id, round_number):
        players = Player.get_players_from_tournament_id(tournament_id)
        start_round_timestamp = self.timestamp()
        round_matchs = self.generate_first_round_matchs(players)
        end_round_timestamp = self.timestamp()
        # Round Creation
        round_name = "Round " + str(round_number)
        new_round = Round(round_number=str(round_number), round_name=round_name, start_date=start_round_timestamp,
                          end_date=end_round_timestamp, round_matchs=round_matchs, flag="Round Finished")

        Round.update_round_in_table(tournament_id, new_round)

    def generate_first_round_matchs(self, players):
        ranked_players = sorted(players, key=lambda x: x.ranking, reverse=True)
        number_of_players = len(ranked_players)
        i = 0
        round_matchs = []
        while 2 * i < number_of_players:
            index1 = i
            index2 = (i + int(number_of_players / 2))
            result = self.view.prompt_input_match_result(ranked_players[index1], ranked_players[index2])
            player_white_result = [ranked_players[index1], Match.translate_match_results(result)[0]]
            player_black_result = [ranked_players[index2], Match.translate_match_results(result)[1]]
            match_result = (player_white_result, player_black_result)
            match = Match(match_result)
            round_matchs.append(match)
            i += 1
        return round_matchs

    def generate_other_round(self, tournament_id, round_number):
        MAX_ROUNDS = 4
        players = Player.get_players_from_tournament_id(tournament_id)
        start_round_timestamp = self.timestamp()
        round_matchs = self.generate_other_round_matchs(players, tournament_id)
        end_round_timestamp = self.timestamp()
        # Round Creation
        round_name = "Round " + str(round_number)
        new_round = Round(round_number=str(round_number), round_name=round_name, start_date=start_round_timestamp,
                          end_date=end_round_timestamp, round_matchs=round_matchs, flag="Round Finished")
        Round.update_round_in_table(tournament_id, new_round)
        if round_number == MAX_ROUNDS:
            self.flag_tournament_finished(tournament_id)

    def generate_other_round_matchs(self, players, tournament_id):
        ranked_players = sorted(
            players, key=lambda x: (
                Player.aggregate_player_score(str(x.get_player_id()), tournament_id), x.ranking), reverse=True)
        self.view.display_players_ranking_in_tournament(ranked_players, tournament_id)
        number_of_players = len(ranked_players)
        i = 0
        round_matchs = []
        while i < number_of_players:
            index1 = i
            index2 = (i + 1)
            result = self.view.prompt_input_match_result(ranked_players[index1], ranked_players[index2])
            player_white_result = [ranked_players[index1], Match.translate_match_results(result)[0]]
            player_black_result = [ranked_players[index2], Match.translate_match_results(result)[1]]
            match_result = (player_white_result, player_black_result)
            match = Match(match_result)
            round_matchs.append(match)
            i += 2
        return round_matchs

    def input_results(self):
        MAX_ROUNDS = 4
        if Tournament.is_table_tournaments_empty():
            self.view.prompt_alert_table_tournaments_empty()
            exit()
        self.view.display_all_tournaments()
        tournament_id = self.view.prompt_choose_tournament_id()
        self.view.display_tournament_rounds(tournament_id)
        if self.is_tournament_over(tournament_id) is False:
            if self.do_i_need_a_new_round(tournament_id):
                new_round = Round.create_empty_new_round_in_tournament(tournament_id)
                Round.append_round_in_table(tournament_id, new_round)
            round_number = self.what_is_latest_round(tournament_id)
            if round_number == 1:
                self.generate_first_round(tournament_id, round_number)
            elif 1 < round_number <= MAX_ROUNDS:
                self.generate_other_round(tournament_id, round_number)
            else:
                self.view.prompt_alert_round_input()
                self.display_sub_menu("2")
        else:
            self.view.prompt_alert_round_input()
            self.display_sub_menu("2")

    def timestamp(self):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return timestamp

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

    def flag_tournament_finished(self, tournament_id):
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
            self.view.display_tournament_rounds(tournament_id)
        elif index == str(7):
            self.view.display_tournament_matchs()
        elif index == str(8):
            self.display_main_menu()
        elif str(index).upper() == "Q":
            exit()
        self.display_sub_menu("3")
