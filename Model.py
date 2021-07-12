class Tournament:

    def __init__(self, name, place, date, rounds, players, timing_type, description, number_of_rounds=4):

        self.name = name
        self.place = place
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.rounds = rounds
        self.players = players
        self.timing_type = timing_type
        self.description = description


class Match:
    def __init__(self, player_white, score_white, player_black, score_black):
        """match initialisation"""
        self.player_white = player_white
        self.score_white = score_white
        self.player_black = player_black
        self.score_black = score_black


class Round:

    def __init__(self, match_instance, round_name, start_date, start_time, end_date, end_time):
        self.match_instance = match_instance
        self.round_name = round_name
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time


class Player:

    def __init__(self, first_name, last_name, date_of_birth, gender, ranking, score=0, played=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.ranking = ranking
        self.score = score
        self.played = played

    #def played(self, player):
    #    self.played(player) = played.append(player)