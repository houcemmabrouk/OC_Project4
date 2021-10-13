from tinydb import TinyDB, Query
from models.player import Player
from controllers.controller import Controller


class View:

    def __init__(self):
        db = TinyDB('db.json')
        self.table_players = db.table("players")
        self.table_tournaments = db.table("tournaments")


    # Vues Menu
    def display_menu(self):
        print("Players...........................................Enter 1 : ")
        print("Tournaments.......................................Enter 2 : ")
        print("Reports...........................................Enter 3 : ")
        print("Quit..............................................Enter Q : ")
        choice = input("Enter Your Choice : ")
        return choice

    def display_menu_players(self):
        print("Create Player.....................................Enter 1 : ")
        print("Update Player Ranking.............................Enter 2 : ")
        print("Display Players...................................Enter 3 : ")
        print("Back To Main Menu.................................Enter 4 : ")
        print("Quit..............................................Enter Q : ")
        choice = input("Enter Your Choice : ")
        return choice

    def display_menu_tournaments(self):
        print("New Tournament....................................Enter 1 : ")
        print("Display Tournaments...............................Enter 2 : ")
        print("Input Results.....................................Enter 3 : ")
        print("Back To Main Menu.................................Enter 4 : ")
        print("Quit..............................................Enter Q : ")
        choice = input("Enter Your Choice : ")
        return choice

    def display_menu_reports(self):
        print("Players in Alphabetic Order.......................Enter 1 : ")
        print("Players by Ranking................................Enter 2 : ")
        print("Tournament Players Alphabetically Ordered ........Enter 3 : ")
        print("Tournament Players Ranking Ordered................Enter 4 : ")
        print("List of All Tournaments...........................Enter 5 : ")
        print("List of Tournament Rounds.........................Enter 6 : ")
        print("List of Tournament Matches........................Enter 7 : ")
        print("Back To Main Menu.................................Enter 8 : ")
        print("Quitter...........................................Enter Q : ")
        choice = input("Enter Your Choice : ")
        return choice

    # Player............................................................................................................

    def prompt_player_info(self):
        first_name = input("Enter Player First Name : ")
        last_name = input("Enter Player Last Name : ")
        date_of_birth = input("Enter Player Date of Birth (dd/mm:yyyy) : ")
        sex = input("Enter Player Sex M for Male / F for Female : ")
        ranking = input("Enter Player Elo Ranking : ")
        tournament_score = 0
        player_info = {'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth,
                       'sex': sex, 'ranking': ranking, 'tournament_score': tournament_score}
        return player_info

    def prompt_player_id_for_update(self):
        player_id = input("Enter the ID of the player you want to Update : ")
        return player_id

    def prompt_input_new_ranking(self):
        new_ranking = input("Enter Player New Ranking : ")
        return new_ranking

    def prompt_modification_success(self):
        print("Ranking Updated Successfully")

    def display_players(self, players_added_in_tournament):
        for player in self.table_players:
            if str(player.doc_id) not in players_added_in_tournament:
                results = str(player.doc_id) + " : " + player["first_name"].capitalize() + " " + \
                          player["last_name"].upper() + " (" + player["ranking"] + ")"
                print(results)

    def prompt_new_tournament(self):
        tournament_name = input("Enter Tournament Name : ")
        place = input("Enter Tournament Place : ")
        start_date = input("Enter Tournament Start Date : ")
        end_date = input("Enter Tournament End Date : ")
        number_of_rounds = 4
        time_control = input("Enter Tournament Time Control ( Blitz / Classical / Rapid ) : ")
        description = input("Enter Tournament Description : ")
        tournament_info = {'tournament_name': tournament_name, 'place': place, 'start_date': start_date,
                           'end_date': end_date, 'number_of_rounds': number_of_rounds, 'time_control': time_control,
                           'description': description
                           }
        return tournament_info

    def prompt_joueur_tournoi(self, i):
        indice = input("Veuillez entrer l'indice du joueur " + str(i) + " : ")
        return indice

    def prompt_input_match_result(self, player_white: Player, player_black: Player,):
        result = input(f"If {player_white.first_name} {player_white.last_name} is the winner Enter 1 \n"
                       f"If {player_black.first_name} {player_black.last_name} is the winner Enter 2 \n"
                       f"If The Match is a Draw Enter x \n"
                       f"Enter The Result : ")
        return result

    # Choices.........................................................................................................

    def prompt_choose_tournament_id(self):
        tournament_id = input("Enter Tournament ID : ")
        return tournament_id

    def prompt_choose_round_id(self):
        round_id = input("Enter Round ID : ")
        return round_id

    # Alerts...........................................................................................................

    def prompt_alert_not_enough_players(self):
        print("You need to create at least 8 players to create a Tournament ")

    def prompt_alert_round_input(self):
        print("You can only input results for the Round in Progress")



    def prompt_add_player_id_to_tournament(self, player_number):
        player_id = input("Please Enter Player Id You Want to Add to Tournament " + str(player_number) + " : ")
        return player_id

    def display_rounds_from_tournament_id(self, tournament_id):
        for tournament_in_table in self.table_tournaments:
            if str(tournament_id) == str(tournament_in_table.doc_id):
                rounds_in_table = tournament_in_table['rounds']
                for round_in_table in rounds_in_table:
                    results = str(round_in_table['round_number']) + " : " + round_in_table['round_name'] + " " + \
                              str(round_in_table['start_date']) + " " + str(round_in_table['end_date']) + " " + \
                              round_in_table['flag']
                    print(results)

    def display_players_not_in_tournament(self, players_added_to_tournament):
        for player in self.table_players:
              if str(player.doc_id) not in players_added_to_tournament:
                results = str(player.doc_id) + " : " + player["first_name"] + " " + \
                          player["last_name"] + " (" + player["ranking"] + ")"
                print(results)

    # Reports...........................................................................................................

    def display_players_alphabetical(self):
        players = []
        for player_in_table in self.table_players:
            player = Player(first_name=player_in_table['first_name'],
                            last_name=player_in_table['last_name'],
                            date_of_birth=player_in_table['date_of_birth'],
                            sex=player_in_table['sex'],
                            ranking=player_in_table['ranking'],
                            tournament_score=player_in_table['tournament_score'])
            players.append(player)

        players = sorted(players, key=lambda x: x.last_name, reverse=False)
        i = 0
        for player in players:
            i += 1
            results = str(i) + " : " + player.last_name + " " + player.first_name + " " + \
                      str(player.date_of_birth) + " " + player.sex + " " + str(player.ranking)
            print(results)

    def display_players_by_ranking(self):
        players = []
        for player_in_table in self.table_players:
            player = Player(first_name=player_in_table['first_name'],
                            last_name=player_in_table['last_name'],
                            date_of_birth=player_in_table['date_of_birth'],
                            sex=player_in_table['sex'],
                            ranking=player_in_table['ranking'],
                            tournament_score=player_in_table['tournament_score'])
            players.append(player)

        players = sorted(players, key=lambda x: x.ranking, reverse=False)
        i = 0
        for player in players:
            i += 1
            results = str(i) + " : " + player.last_name + " " + player.first_name + " " + \
                      str(player.date_of_birth) + " " + player.sex + " " + str(player.ranking)
            print(results)

    def display_tournament_players_alphabetical(self):
        self.display_all_tournaments()
        players = []
        tournament_id = self.prompt_choose_tournament_id()
        tournament = self.table_tournaments.get(doc_id=int(tournament_id))
        players_ids = tournament['players']
        for players_id in players_ids:
            player = Player.get_player_from_id(players_id)
            players.append(player)
        i = 0
        players = sorted(players, key=lambda x: x.last_name, reverse=False)
        for player in players:
            i += 1
            results = str(i) + " : " + player.last_name + " " + player.first_name + " " + player.date_of_birth + " " + \
                      player.sex + " (" + player.ranking + ")"
            print(results)

    def display_tournaments_players_by_ranking(self):
        self.display_all_tournaments()
        players = []
        tournament_id = self.prompt_choose_tournament_id()
        tournament = self.table_tournaments.get(doc_id=int(tournament_id))
        players_ids = tournament['players']
        for players_id in players_ids:
            player = Player.get_player_from_id(players_id)
            players.append(player)
        players = sorted(players, key=lambda x: x.ranking, reverse=False)
        i = 0
        for player in players:
            i += 1
            results = str(i) + " : (" + str(player.ranking) + ") " + player.first_name + " " + \
                      player.last_name + " " + str(player.date_of_birth) + " " + player.sex
            print(results)

    def display_all_tournaments(self):
        for tournament_in_table in self.table_tournaments:
            results = str(tournament_in_table.doc_id) + " : " + tournament_in_table["tournament_name"] + " " + \
                      tournament_in_table["place"] + " (" + tournament_in_table["start_date"] + ")" + " " + \
                      tournament_in_table["flag"]
            print(results)

    def display_tournament_rounds(self, tournament_id):
        for tournament_in_table in self.table_tournaments:
            if str(tournament_id) == str(tournament_in_table.doc_id):
                rounds_in_table = tournament_in_table['rounds']
                for round_in_table in rounds_in_table:
                    results = str(round_in_table['round_number']) + " : " + round_in_table['round_name'] + " " + \
                              str(round_in_table['start_date']) + " " + str(round_in_table['end_date']) + " " + \
                              round_in_table['flag']
                    print(results)

    def display_tournament_matchs(self):
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
                              str(player_white.last_name)).ljust(23, ".") + " " + str(score_white)) + "  -  " +
                              (str(player_black.first_name) + " " + str(player_black.last_name)).ljust(23, ".")
                              + " " + str(score_black))
                    match_id += 1
                    print(results)