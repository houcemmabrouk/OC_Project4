from tinydb import TinyDB
from models.match import Match


db = TinyDB('db.json')
table_tournaments = db.table("tournaments")


class Round:

    def __init__(self, round_number, round_name, start_date, end_date, round_matchs, flag):
        self.round_number = round_number
        self.round_name = round_name
        self.start_date = start_date
        self.end_date = end_date
        self.round_matchs = round_matchs
        self.flag = flag

    def serialize_round(self):
        serialized_matchs = []

        for match_in_round in self.round_matchs:
            serialized_match = match_in_round.serialize_match()
            serialized_matchs.append(serialized_match)

        serialized_round = {
                            'round_number': self.round_number,
                            'round_name': self.round_name,
                            'start_date': self.start_date,
                            'end_date': self.end_date,
                            'round_matchs': serialized_matchs,
                            'flag': self.flag,
                            }
        return serialized_round

    def deserialize_round_cls(cls, serialized_round):
        rounds = []
        round_matchs = []
        for round_in_table in serialized_round['round_matchs']:
            print(round_in_table)
            for match_in_table in round_in_table:
                deserialized_match = Match.deserialize_match(match_in_table)
                round_matchs.append(deserialized_match)
            rounds.append(round_matchs)

        round = Round(round_number=serialized_round['round_number'],
                      round_name=serialized_round['round_name'],
                      start_date=serialized_round['start_date'],
                      end_date=serialized_round['end_date'],
                      round_matchs=round_matchs,
                      flag=serialized_round['flag']
                      )
        return round

    deserialize_round = classmethod(deserialize_round_cls)

    def get_rounds_from_tournament_id_cls(cls, tournament_id):
        rounds_in_tournament_table = table_tournaments.get(doc_id=int(tournament_id))['rounds']
        return rounds_in_tournament_table

    get_rounds_from_tournament_id = classmethod(get_rounds_from_tournament_id_cls)

    def get_round_flag_cls(cls, round_number, tournament_id):
        flag = "Not Found"
        for tournament_in_table in table_tournaments:
            if str(tournament_in_table.doc_id) == str(tournament_id):
                rounds_in_table = tournament_in_table['rounds']
                for round_in_table in rounds_in_table:
                    if round_in_table['round_number'] == str(round_number):
                        flag = round_in_table['flag']
                        return flag

    get_round_flag = classmethod(get_round_flag_cls)

    def last_round_index_in_table_cls(cls, tournament_id):
        """returns length of round list in a tournament"""
        tournament_in_table = table_tournaments.get(doc_id=int(tournament_id))
        last_round_index = len(tournament_in_table['rounds'])
        return last_round_index

    last_round_index_in_table = classmethod(last_round_index_in_table_cls)

    def create_empty_new_round_in_tournament_cls(cls, tournament_id):
        """returns an empty new round for a given tournament"""
        last_round = Round.last_round_index_in_table(tournament_id)
        new_round_number = int(last_round) + 1
        round_number = str(new_round_number)
        round_name = "Round " + str(new_round_number)
        start_date = "Not Assigned"
        end_date = "Not Assigned"
        round_matchs = []
        flag = "In Progress"
        new_round = Round(round_number, round_name, start_date, end_date, round_matchs, flag)
        return new_round

    create_empty_new_round_in_tournament = classmethod(create_empty_new_round_in_tournament_cls)

    def append_round_in_table_cls(cls, tournament_id, round):
        rounds_in_tournament_table = Round.get_rounds_from_tournament_id(tournament_id)
        rounds_in_tournament_table.append(round.serialize_round())
        tournament_in_table = table_tournaments.get(doc_id=int(tournament_id))
        table_tournaments.update({"rounds": rounds_in_tournament_table}, doc_ids=[tournament_in_table.doc_id])

    append_round_in_table = classmethod(append_round_in_table_cls)

    def update_round_in_table_cls(cls, tournament_id, round):
        rounds_in_tournament_table = Round.get_rounds_from_tournament_id(tournament_id)
        rounds_in_tournament_table.pop()
        rounds_in_tournament_table.append(round.serialize_round())
        tournament_in_table = table_tournaments.get(doc_id=int(tournament_id))
        table_tournaments.update({"rounds": rounds_in_tournament_table}, doc_ids=[tournament_in_table.doc_id])

    update_round_in_table = classmethod(update_round_in_table_cls)

    def create_new_match(self, matchs):
        self.round_matchs.append(matchs)
