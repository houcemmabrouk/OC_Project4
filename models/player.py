from tinydb import TinyDB, Query
from typing import List

db = TinyDB('db.json')
table_players = db.table("players")
table_tournaments = db.table("tournaments")


class Player:

    def __init__(self, first_name, last_name, date_of_birth, sex, ranking, tournament_score):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking
        self.tournament_score = tournament_score
        self.players: List[Player] = []

    def update_ranking(self, new_value):
        """updates object attribute"""
        self.ranking = new_value

    def serialize_player(self):
        serialized_player = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'sex': self.sex,
            'ranking': self.ranking,
            'tournament_score': self.tournament_score
        }
        return serialized_player

    def deserialize_player(self, serialized_player):
        player = Player(
            first_name=serialized_player['first_name'],
            last_name=serialized_player['last_name'],
            date_of_birth=serialized_player['date_of_birth'],
            sex=serialized_player['sex'],
            ranking=serialized_player['ranking'],
            tournament_score=serialized_player['tournament_score']
        )
        return player

    def get_player_id(self):
        """Search for player id in the database"""
        User = Query()
        serialized_player = self.serialize_player()
        documents = table_players.search(User.first_name == str(serialized_player['first_name']) and
                                         User.last_name == str(serialized_player['last_name']) and
                                         User.date_of_birth == str(serialized_player['date_of_birth']))
        id_player = None
        for document in documents:
            id_player = document.doc_id
        return id_player

    def get_players_ids_cls(cls, players):
        players_ids = []
        for player in players:
            player_id = player.get_player_id()
            players_ids.append(player_id)
        return players_ids

    get_players_ids = classmethod(get_players_ids_cls)

    def save(self):
        serialized_player = self.serialize_player()
        table_players.insert(serialized_player)

    def get_player_from_id_cls(cls, player_id):
        """returns player object from an id. The id can be either string or integer"""
        for player_in_table in table_players:
            if str(player_id) == str(player_in_table.doc_id):
                player = Player(
                    player_in_table['first_name'],
                    player_in_table['last_name'],
                    player_in_table['date_of_birth'],
                    player_in_table['sex'],
                    player_in_table['ranking'],
                    player_in_table['tournament_score']
                )
                return player

    get_player_from_id = classmethod(get_player_from_id_cls)

    def get_players_from_ids_cls(cls, players_ids):
        players: List[Player] = []
        for player_id in players_ids:
            player = Player.get_player_from_id(player_id)
            players.append(player)
        return players

    get_players_from_ids = classmethod(get_players_from_ids_cls)

    def get_new_player_cls(cls, player_info):
        player = Player(first_name=player_info['first_name'].capitalize(), last_name=player_info['last_name'].upper(),
                        date_of_birth=player_info['date_of_birth'], sex=player_info['sex'].upper(),
                        ranking=player_info['ranking'], tournament_score=player_info['tournament_score'])
        return player

    get_new_player = classmethod(get_new_player_cls)

    def check_player_id_cls(self, player_id):
        for player in table_players:
            if str(player.doc_id) == player_id:
                return True

    check_player_id = classmethod(check_player_id_cls)

    def number_of_players_in_db_cls(cls):
        number_of_players = 0
        for player in table_players:
            if player.doc_id is not None:
                number_of_players += 1
        return number_of_players

    number_of_players_in_db = classmethod(number_of_players_in_db_cls)

    def get_players_from_tournament_id_cls(cls, tournament_id):
        tournament_in_table = table_tournaments.get(doc_id=int(tournament_id))
        players = Player.get_players_from_ids(tournament_in_table['players'])
        return players

    get_players_from_tournament_id = classmethod(get_players_from_tournament_id_cls)

    @staticmethod
    def is_table_players_empty():
        if len(table_players.all()) == 0:
            return True

    @staticmethod
    def aggregate_player_score(player_id, tournament_id):
        player_score = 0.0
        for tournament_in_table in table_tournaments:
            if str(tournament_id) == str(tournament_in_table.doc_id):
                rounds_in_table = tournament_in_table['rounds']
                for round_in_table in rounds_in_table:
                    matchs_in_table = round_in_table['round_matchs']
                    for match_in_table in matchs_in_table:
                        if str(match_in_table['result'][0][0]) == player_id:
                            player_score += match_in_table['result'][0][1]
                        if str(match_in_table['result'][1][0]) == player_id:
                            player_score += match_in_table['result'][1][1]
        return player_score
