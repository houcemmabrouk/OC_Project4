from models.round import Round
from models.player import Player
from tinydb import TinyDB, Query
from typing import List

db = TinyDB('db.json')
table_tournaments = db.table("tournaments")
table_players = db.table("players")


class Tournament:

    def __init__(self, tournament_name, place, start_date, end_date, number_of_rounds, time_control,
                 description, players, rounds, flag):

        self.tournament_name = tournament_name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.time_control = time_control
        self.description = description
        self.players = players
        self.players: List[Player] = []
        self.rounds = rounds
        self.rounds: List[Round] = []
        self.flag = flag

    def serialize_tournament(self):
        serialized_rounds = []
        for round_in_tournament in self.rounds:
            serialized_round = Round.serialize_round(round_in_tournament)
            serialized_rounds.append(serialized_round)

        serialized_tournament = {'tournament_name': self.tournament_name,
                                 'place': self.place,
                                 'start_date': self.start_date,
                                 'end_date': self.end_date,
                                 'number_of_rounds': self.number_of_rounds,
                                 'time_control': self.time_control,
                                 'description': self.description,
                                 'players': Player.get_players_ids(self.players),
                                 'rounds': serialized_rounds,
                                 'flag': self.flag
                                 }
        return serialized_tournament

    def deserialize_tournament_cls(self, serialized_tournament):
        self.tournament_name = serialized_tournament['tournament_name']
        self.place = serialized_tournament['place']
        self.start_date = serialized_tournament['start_date']
        self.end_date = serialized_tournament['end_date']
        self.number_of_rounds = serialized_tournament['number_of_rounds']
        self.time_control = serialized_tournament['time_control']
        self.description = serialized_tournament['description']
        self.players = Player.get_players_from_ids(serialized_tournament['players'])
        # PROBLEM Round.deserialize_round(serialized_tournament['rounds'])
        # PROBLEM serialized_tournament['rounds']
        self.rounds = serialized_tournament['rounds']

    deserialize_tournament = classmethod(deserialize_tournament_cls)

    def get_tournament_id(self):
        """Search for tournament id in the database"""
        User = Query()
        serialized_tournament = self.serialize_tournament()
        documents = table_tournaments.search(User.tournament_name == str(serialized_tournament['tournament_name'])
                                             and User.start_date == str(serialized_tournament['start_date']))
        id_tournament = None
        for document in documents:
            id_tournament = document.doc_id
        return id_tournament

    def get_tournament_from_id_cls(cls, tournament_id):
        for tournament_in_table in table_tournaments:
            if str(tournament_id) == str(tournament_in_table.doc_id):
                tournament = Tournament(tournament_name=tournament_in_table['tournament_name'],
                                        place=tournament_in_table['place'],
                                        start_date=tournament_in_table['start_date'],
                                        end_date=tournament_in_table['end_date'],
                                        number_of_rounds=tournament_in_table['number_of_rounds'],
                                        time_control=tournament_in_table['time_control'],
                                        description=tournament_in_table['description'],
                                        players=Player.get_players_from_ids(tournament_in_table['players']),
                                        # PROBLEM Round.deserialize_round(tournament_in_table['rounds'])
                                        # PROBLEM rounds=tournament_in_table['rounds']
                                        rounds=Round.deserialize_round(tournament_in_table['rounds']),
                                        flag=tournament_in_table['flag']
                                        )
                return tournament

    get_tournament_from_id = classmethod(get_tournament_from_id_cls)

    def get_tournament_last_round_number_cls(cls, tournament_id):
        i = 0
        last_round = 1
        for tournament_in_table in table_tournaments:
            if str(tournament_in_table.doc_id) == tournament_id:
                rounds_in_table = tournament_in_table['rounds']
                for round_in_table in rounds_in_table:
                    i += 1
                    last_round = i
        return last_round

    get_tournament_last_round_number = classmethod(get_tournament_last_round_number_cls)

    @staticmethod
    def is_table_tournaments_empty():
        if len(table_tournaments.all()) == 0:
            return True
