from models.player import Player


class Match:

    def __init__(self, result):
        self.result = result

    def serialize_match(self):
        """returns from a match object a serialized match as a dictionary"""
        player_white_id = (self.result[0][0]).get_player_id()
        score_white = self.result[0][1]
        player_black_id = (self.result[1][0]).get_player_id()
        score_black = self.result[1][1]
        match_result = ([player_white_id, score_white], [player_black_id, score_black])
        serialized_match = {'result': match_result}
        return serialized_match

    def serialize_matchs_cls(cls, matchs):
        serialized_matchs = []
        for match in matchs:
            player_white_id = (match.result[0][0]).get_player_id()
            score_white = match.result[0][1]
            player_black_id = (match.result[1][0]).get_player_id()
            score_black = match.result[1][1]
            match_result = ([player_white_id, score_white], [player_black_id, score_black])
            serialized_match = {'result': match_result}
            serialized_matchs.append(serialized_match)
        return serialized_matchs

    serialize_matchs = classmethod(serialize_matchs_cls)

    def deserialize_match_cls(cls, serialized_match):
        player_white = Player.get_player_from_id(serialized_match[0][0])
        score_white = serialized_match[0][1]
        player_black = Player.get_player_from_id(serialized_match[1][0])
        score_black = serialized_match[1][1]
        match_result = ([player_white, score_white], [player_black, score_black])
        match = Match(match_result)
        return match

    deserialize_match = classmethod(deserialize_match_cls)
