from tinydb import TinyDB
from models.player import Player
from models.tournament import Tournament
from views.ask import ask_date
from views.ask import ask_integer
from views.ask import ask_string
from views.ask import ask_choice
import datetime


class View:

    def __init__(self):
        db = TinyDB('db.json')
        self.table_players = db.table("players")
        self.table_tournaments = db.table("tournaments")

    """Menu functions"""

    def display_menu(self):
        """This function displays main menu"""
        print("Players...........................................Enter 1 : ")
        print("Tournaments.......................................Enter 2 : ")
        print("Reports...........................................Enter 3 : ")
        print("Quit..............................................Enter Q : ")
        choice = ask_choice(["1", "2", "3", "Q"], "")
        return choice

    def display_menu_players(self):
        """This function displays player menu and gets user choice in that menu"""
        print("Create Player.....................................Enter 1 : ")
        print("Update Player Ranking.............................Enter 2 : ")
        print("Display Players...................................Enter 3 : ")
        print("Back To Main Menu.................................Enter 4 : ")
        print("Quit..............................................Enter Q : ")
        choice = ask_choice(["1", "2", "3", "4", "5", "Q"], "")
        return choice

    def display_menu_tournaments(self):
        """This function displays tournaments menu and gets user choice in that menu"""
        print("New Tournament....................................Enter 1 : ")
        print("Display Tournaments...............................Enter 2 : ")
        print("Input Results.....................................Enter 3 : ")
        print("Back To Main Menu.................................Enter 4 : ")
        print("Quit..............................................Enter Q : ")
        choice = ask_choice(["1", "2", "3", "4", "Q"], "")
        return choice

    def display_menu_reports(self):
        """This function displays reports menu and gets user choice in that menu"""
        print("Players in Alphabetic Order.......................Enter 1 : ")
        print("Players by Ranking................................Enter 2 : ")
        print("Tournament Players Alphabetically Ordered ........Enter 3 : ")
        print("Tournament Players Ranking Ordered................Enter 4 : ")
        print("List of All Tournaments...........................Enter 5 : ")
        print("List of Tournament Rounds.........................Enter 6 : ")
        print("List of Tournament Matches........................Enter 7 : ")
        print("Back To Main Menu.................................Enter 8 : ")
        print("Quitter...........................................Enter Q : ")
        choice = ask_choice(["1", "2", "3", "4", "5", "6", "7", "8", "Q"], "")
        return choice

    """Database Alerts"""

    def prompt_alert_table_tournaments_empty(self):
        print("Table tournaments is empty")

    def prompt_alert_table_players_emty(self):
        print("Table players is empty")

    """Player functions"""

    def prompt_player_info(self):
        """This function gathers player information which is returned in player_info dictionary"""
        first_name = ask_string(2, 20, "Enter Player First Name : ").capitalize()
        last_name = ask_string(2, 20, "Enter Player Last Name : ").upper()
        date_of_birth = ask_date(datetime.date(1900, 1, 1), datetime.date.today(),
                                 "Enter Player Date of Birth (dd/mm:yyyy) : ")
        sex = ask_choice(["M", "F"], "Enter Player Sex M for Male / F for Female : ")
        ranking = ask_integer(0, 4000, "Enter Player Elo Ranking : ")
        tournament_score = 0
        player_info = {'first_name': first_name, 'last_name': last_name, 'date_of_birth': str(date_of_birth),
                       'sex': sex, 'ranking': ranking, 'tournament_score': tournament_score}
        return player_info

    def prompt_player_id_for_update(self):
        """This function gets player_id which is used to update player ranking"""
        player_id = ask_integer(1, 100000, "Enter the ID of the player you want to Update : ")
        return player_id

    def prompt_input_new_ranking(self):
        """This function gets new ranking value which is used to update player ranking"""
        new_ranking = ask_integer(0, 4000, "Enter Player New Ranking : ")
        return new_ranking

    def prompt_modification_success(self):
        print("Ranking Updated Successfully")

    def display_players(self, players_added_in_tournament):
        """This function displays all players info except the players given in argument"""
        for i, p in enumerate(self.table_players, start=1):
            if str(p.doc_id) not in players_added_in_tournament:
                print(f"{i}: {p['first_name'].ljust(15)} {p['last_name'].ljust(15)} {p['ranking']} {p['date_of_birth']}"
                      f" {p['sex']}")

    """New tournament functions"""

    def prompt_new_tournament(self):
        """This function gathers new tournament information which is returned in tournament_info dictionary"""
        tournament_name = ask_string(4, 50, "Enter Tournament Name : ")
        place = ask_string(4, 50, "Enter Tournament Place : ")
        start_date = ask_date(datetime.date(1900, 1, 1), datetime.date(2100, 1, 1), "Enter Tournament Start Date : ")
        end_date = ask_date(start_date, datetime.date(2100, 1, 1), "Enter Tournament End Date : ")
        number_of_rounds = 4
        time_control = ask_choice(["BLITZ", "CLASSICAL", "RAPID"],
                                  "Enter Tournament Time Control ( Blitz / Classical / Rapid ) : ")
        description = ask_string(4, 250, "Enter Tournament Description : ")
        tournament_info = {'tournament_name': tournament_name, 'place': place, 'start_date': str(start_date),
                           'end_date': str(end_date), 'number_of_rounds': str(number_of_rounds),
                           'time_control': time_control, 'description': description}
        return tournament_info

    def prompt_add_player_id_to_tournament(self, player_number):
        """This function gets player_id which is used to update player ranking"""
        player_id = ask_integer(
            1, 100000, "Please Enter Player Id You Want to Add to Tournament " + str(player_number) + " : ")
        return player_id

    """Input results"""

    def prompt_input_match_result(self, player_white: Player, player_black: Player):
        """This function prompts players name for each match and gets match result"""
        result = ask_choice(
            ["1", "2", "X"], f"If {player_white.first_name} {player_white.last_name} is the winner Enter 1 \n"
                             f"If {player_black.first_name} {player_black.last_name} is the winner Enter 2 \n"
                             f"If The Match is a Draw Enter x")
        return result

    def prompt_alert_not_enough_players(self):
        """This function prompts an alert if a the user try's to launch a new tournament and the database
         has less than 8 players"""
        print("You need to create at least 8 players to create a Tournament ")

    def prompt_choose_tournament_id(self):
        """This function gets tournament_id used to input results or to be displayed in reports"""
        tournament_id = ask_integer(0, 100000, "Enter Tournament ID : ")
        return tournament_id

    def prompt_choose_round_id(self):
        """This function gets round_id to be displayed in reports"""
        round_id = ask_integer(0, 100000, "Enter Round ID : ")
        return round_id

    def prompt_alert_round_input(self):
        """This function prompts an alert if there is an error in round number used to input results"""
        print("You can only input results for the Last Round in Progress")

    """Reports"""

    def display_players_alphabetical(self):
        players = []
        for player in self.table_players:
            player = Player(player['first_name'], player['last_name'], player['date_of_birth'], player['sex'],
                            player['ranking'], player['tournament_score'])
            players.append(player)
        players = sorted(players, key=lambda x: x.last_name, reverse=False)
        for i, p in enumerate(players, start=1):
            print(f"{i}: {p.last_name.ljust(15)} {p.first_name.ljust(15)} {p.date_of_birth} {p.sex} {p.ranking}")

    def display_players_by_ranking(self):
        players = []
        for player in self.table_players:
            player = Player(player['first_name'], player['last_name'], player['date_of_birth'], player['sex'],
                            player['ranking'], player['tournament_score'])
            players.append(player)
        players = sorted(players, key=lambda x: x.ranking, reverse=True)
        for i, p in enumerate(players, start=1):
            print(f"{i}: {p.last_name.ljust(15)} {p.first_name.ljust(15)} {p.date_of_birth} {p.sex} ({p.ranking})")

    def display_tournament_players_alphabetical(self):
        if not Player.is_table_players_empty():
            self.display_all_tournaments()
            players = []
            tournament_id = self.prompt_choose_tournament_id()
            tournament = self.table_tournaments.get(doc_id=int(tournament_id))
            players_ids = tournament['players']
            for players_id in players_ids:
                player = Player.get_player_from_id(players_id)
                players.append(player)
            players = sorted(players, key=lambda x: x.last_name, reverse=False)
            for i, p in enumerate(players, start=1):
                print(f"{i}: {p.last_name.ljust(15)} {p.first_name.ljust(15)} {p.date_of_birth} {p.sex} {p.ranking}")
        else:
            self.prompt_alert_table_players_emty()

    def display_tournaments_players_by_ranking(self):
        if not Player.is_table_players_empty():
            self.display_all_tournaments()
            players = []
            tournament_id = self.prompt_choose_tournament_id()
            tournament = self.table_tournaments.get(doc_id=int(tournament_id))
            players_ids = tournament['players']
            for players_id in players_ids:
                player = Player.get_player_from_id(players_id)
                players.append(player)
            players = sorted(players, key=lambda x: x.ranking, reverse=True)
            for i, p in enumerate(players, start=1):
                print(f"{i}: {p.last_name.ljust(15)} {p.first_name.ljust(15)} {p.date_of_birth} {p.sex} ({p.ranking})")
        else:
            self.prompt_alert_table_players_emty()

    def display_all_tournaments(self):
        if not Tournament.is_table_tournaments_empty():
            for i, t in enumerate(self.table_tournaments, start=1):
                print(f"{i}: {t['tournament_name'].ljust(34)} {t['place'].ljust(12)} {t['start_date']} {t['flag']}")
        else:
            self.prompt_alert_table_tournaments_empty()

    def display_tournament_rounds(self, tournament_id):
        if not Tournament.is_table_tournaments_empty():
            for tournament_in_table in self.table_tournaments:
                if str(tournament_id) == str(tournament_in_table.doc_id):
                    rounds_in_table = tournament_in_table['rounds']
                    for i, r in enumerate(rounds_in_table, start=1):
                        print(f"{r['round_number']}: {r['round_name']} {r['start_date']} {r['end_date']} {r['flag']}")
        else:
            self.prompt_alert_table_tournaments_empty()

    def display_tournament_matchs(self):
        if not Tournament.is_table_tournaments_empty():
            self.display_all_tournaments()
            tournament_id = self.prompt_choose_tournament_id()
            tournament = self.table_tournaments.get(doc_id=int(tournament_id))
            self.display_tournament_rounds(tournament_id)
            round_id = self.prompt_choose_round_id()
            rounds_in_table = tournament['rounds']
            match_id = 1
            for round_in_table in rounds_in_table:
                if round_in_table['round_number'] == round_id:
                    tournament_matchs = round_in_table['round_matchs']
                    for match_in_table in tournament_matchs:
                        player_white = Player.get_player_from_id(match_in_table['result'][0][0])
                        player_black = Player.get_player_from_id(match_in_table['result'][1][0])
                        score_white = match_in_table['result'][0][1]
                        score_black = match_in_table['result'][1][1]
                        results = str(match_id) + " : " + (((str(player_white.first_name) + " " +
                                                             str(player_white.last_name)
                                                             ).ljust(23, ".") + " " + str(score_white).ljust(3, " ")
                                                            ) + "  -  " +
                                                           (str(player_black.first_name) + " " +
                                                            str(player_black.last_name)
                                                            ).ljust(23, ".") + " " + str(score_black).ljust(3, " ")
                                                           )
                        match_id += 1
                        print(results)
        else:
            self.prompt_alert_table_tournaments_empty()

    def display_players_ranking_in_tournament(self, ranked_players, tournament_id):
        print("R: First Name      Last Name     Score Ranking")
        for i, p in enumerate(ranked_players, start=1):
            player_id = p.get_player_id()
            aggregate_player_score = Player.aggregate_player_score(str(player_id), tournament_id)
            print(f"{i}: {p.first_name.ljust(15)} {p.last_name.ljust(15)} {aggregate_player_score} ({p.ranking}) ")
