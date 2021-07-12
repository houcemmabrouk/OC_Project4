import random

import Controller
import Model
import View
from Model import Match
from Model import Round
from Model import Player
from Model import Tournament





if __name__ == '__main__':
    val = random.sample([0, 0.5, 1], k=3)
    pos = random.randrange(0, 1, 2)

    player1 = Player(first_name=View.player1_first_name,
                           last_name=View.player1_last_name,
                           date_of_birth=View.player1_date_of_birth,
                           gender=View.player1_gender,
                           ranking=View.player1_ranking,
                           score=0
                           )
    player2 = Player(first_name=View.player2_first_name,
                           last_name=View.player2_last_name,
                           date_of_birth=View.player2_date_of_birth,
                           gender=View.player2_gender,
                           ranking=View.player2_ranking,
                           score=0
                           )
    player3 = Player(first_name=View.player3_first_name,
                           last_name=View.player3_last_name,
                           date_of_birth=View.player3_date_of_birth,
                           gender=View.player3_gender,
                           ranking=View.player3_ranking,
                           score=0
                           )
    player4 = Player(first_name=View.player4_first_name,
                           last_name=View.player4_last_name,
                           date_of_birth=View.player4_date_of_birth,
                           gender=View.player4_gender,
                           ranking=View.player4_ranking,
                           score=0
                           )
    player5 = Player(first_name=View.player5_first_name,
                           last_name=View.player5_last_name,
                           date_of_birth=View.player5_date_of_birth,
                           gender=View.player5_gender,
                           ranking=View.player5_ranking,
                           score=0
                           )
    player6 = Player(first_name=View.player6_first_name,
                           last_name=View.player6_last_name,
                           date_of_birth=View.player6_date_of_birth,
                           gender=View.player6_gender,
                           ranking=View.player6_ranking,
                           score=0
                           )
    player7 = Player(first_name=View.player7_first_name,
                           last_name=View.player7_last_name,
                           date_of_birth=View.player7_date_of_birth,
                           gender=View.player7_gender,
                           ranking=View.player7_ranking,
                           score=0
                           )
    player8 = Player(first_name=View.player8_first_name,
                           last_name=View.player8_last_name,
                           date_of_birth=View.player8_date_of_birth,
                           gender=View.player8_gender,
                           ranking=View.player8_ranking,
                           score=0
                           )

    players = [player1, player2, player3, player4, player5, player6, player7, player8]

    tournament_instance = Tournament(name=View.tournament_name,
                                    place=View.tournament_place,
                                    date=View.tournament_date,
                                    number_of_rounds=4,
                                    rounds=[],
                                    players=players,
                                    timing_type=View.tournament_timing_type,
                                    description=View.tournament_description,
                                    )

    player_w = player1
    player_b = player2

    match = Match(player_white=player_w, score_white=0, player_black=player_b, score_black=0)
    match = (player_w, 0, player_b, 0)


    players = sorted(players, key=lambda x: x.ranking, reverse=True)

    round_list = []

    # ROUND 1
    #point_player1 = input("Enter score for " + players[0].first_name + " " + players[0].last_name)
    #players[0].score = float(point_player1)
    point_player1 = 0.5
    players[0].score = float(point_player1)
    point_player2 = 0.5
    players[1].score = point_player2
    point_player3 = 1
    players[2].score = point_player3
    point_player4 = 0.5
    players[3].score = point_player4
    point_player5 = 0
    players[4].score = point_player5
    point_player6 = 1
    players[5].score = point_player6
    point_player7 = 0.5
    players[6].score = point_player7
    point_player8 = 0.5
    players[7].score = point_player8

    # Faire ca automatiquement
    # insatance de Match match de 4 valeurs on doit recuperer un resultat au format ci dessous par une methode

    match1 = Match(players[0], point_player1, players[4], point_player5)
    match2 = Match(players[1], point_player2, players[5], point_player6)
    match3 = Match(players[2], point_player3, players[6], point_player7)
    match4 = Match(players[3], point_player4, players[7], point_player8)


    #print(players[4].first_name)

    matchs = [match1, match2, match3, match4]
    round1 = Round(match_instance=matchs, round_name="Round1",
                   start_date=View.round1_start_date, start_time=View.round1_start_time,
                   end_date=View.round1_end_date, end_time=View.round1_end_time
                   )
    round_list.append(round1)
    tournament_instance.rounds.append(round1)
    rounds = tournament_instance.rounds


    def result_reader():
        i = -1
        for player in players:
            i += 1
            print(players[i].first_name)
            print(players[i].ranking)
            print(players[i].score)

    def has_played(player_searched, player_opponent):
        answer = False
        exchange = []
        for round in round_list:
            for match in round.match_instance:
                if match.player_white == player_searched:
                    played = match.player_black
                    if played == player_opponent:
                        answer = True
                        print(played)
                        exchange = exchange.append(played)
                elif match.player_black == player_searched:
                    played = match.player_white
                    if played == player_opponent:
                        answer = True
                        exchange = exchange.append(played)
        return [answer, exchange]

    def play_control():
        print(has_played(players[0], players[1]))
        print(has_played(players[2], players[3]))
        print(has_played(players[4], players[5]))
        print(has_played(players[6], players[7]))



    players = sorted(players, key=lambda x: (x.score, x.ranking), reverse=True)

    if has_played(players[0], players[1]) == False:
        match5 = Match(players[0], players[0].score, players[1], players[1].score)
    else:
        match5 = Match(players[0], players[0].score, players[2], players[2].score)

    if has_played(players[2], players[3]) == False:
        match6 = Match(players[2], players[2].score, players[3], players[3].score)
    else:
        match6 = Match(players[2], players[2].score, players[4], players[4].score)

    if has_played(players[4], players[5]) == False:
        match7 = Match(players[4], players[4].score, players[5], players[5].score)
    else:
        match7 = Match(players[4], players[4].score, players[6], players[6].score)

    if has_played(players[6], players[7]) == False:
        match8 = Match(players[6], players[6].score, players[7], players[7].score)
    else:
        match8 = Match(players[7], players[7].score, players[0], players[0].score)




    # ROUND 2
    point_player0 = val[pos]
    players[0].score = players[0].score + float(point_player0)
    point_player1 = val[pos]
    players[1].score = players[1].score + point_player1
    point_player2 = val[pos]
    players[2].score = players[2].score + point_player2
    point_player3 = val[pos]
    players[3].score = players[3].score + point_player3
    point_player4 = val[pos]
    players[4].score = players[4].score + point_player4
    point_player5 = val[pos]
    players[5].score = players[5].score + point_player5
    point_player6 = val[pos]
    players[6].score = players[6].score + point_player6
    point_player7 = val[pos]
    players[7].score = players[7].score + point_player7

    match5 = Match(players[0], point_player1, players[4], point_player5)
    match6 = Match(players[1], point_player2, players[5], point_player6)
    match7 = Match(players[2], point_player3, players[6], point_player7)
    match8 = Match(players[3], point_player4, players[7], point_player8)

    round2_matchs = [match5, match6, match7, match8]
    round2 = Round(match_instance=round2_matchs, round_name="Round2",
                   start_date=View.round1_start_date, start_time=View.round1_start_time,
                   end_date=View.round1_end_date, end_time=View.round1_end_time
                   )
    tournament_instance.rounds.append(round2)
    round_list.append(round2)







    # ROUND 3
    players = sorted(players, key=lambda x: (x.score, x.ranking), reverse=True)

    #print(has_played(players[0], players[1]))
    #print(has_played(players[2], players[3]))
    #print(has_played(players[4], players[5]))
    #print(has_played(players[6], players[7]))

    if has_played(players[0], players[1]) == False:
        match9 = Match(players[0], players[0].score, players[1], players[1].score)
    else:
        match9 = Match(players[0], players[0].score, players[2], players[2].score)
    if has_played(players[2], players[3]) == False:
        match10 = Match(players[2], players[2].score, players[3], players[3].score)
    else:
        match10 = Match(players[2], players[2].score, players[4], players[4].score)
    if has_played(players[4], players[5]) == False:
        match11 = Match(players[4], players[4].score, players[5], players[5].score)
    else:
        match11 = Match(players[4], players[4].score, players[6], players[6].score)
    if has_played(players[6], players[7]) == False:
        match12 = Match(players[6], players[6].score, players[7], players[7].score)
    else:
        match12 = Match(players[7], players[7].score, players[0], players[0].score)


    point_player0 = val[pos]
    players[0].score = players[0].score + float(point_player0)
    point_player1 = val[pos]
    players[1].score = players[1].score + point_player1
    point_player2 = val[pos]
    players[2].score = players[2].score + point_player2
    point_player3 = val[pos]
    players[3].score = players[3].score + point_player3
    point_player4 = val[pos]
    players[4].score = players[4].score + point_player4
    point_player5 = val[pos]
    players[5].score = players[5].score + point_player5
    point_player6 = val[pos]
    players[6].score = players[6].score + point_player6
    point_player7 = val[pos]
    players[7].score = players[7].score + point_player7

    match9 = Match(players[0], point_player1, players[4], point_player5)
    match10 = Match(players[1], point_player2, players[5], point_player6)
    match11 = Match(players[2], point_player3, players[6], point_player7)
    match12 = Match(players[3], point_player4, players[7], point_player8)

    round3_matchs = [match9, match10, match11, match12]
    round3 = Round(match_instance=round3_matchs, round_name="Round3",
                   start_date=View.round1_start_date, start_time=View.round1_start_time,
                   end_date=View.round1_end_date, end_time=View.round1_end_time
                   )
    tournament_instance.rounds.append(round3)
    round_list.append(round3)





    players = sorted(players, key=lambda x: (x.score, x.ranking), reverse=True)

    #i = -1
    #for player in players:
    #    i += 1
    #    print(players[i].first_name)
    #    print(players[i].ranking)
    #    print(players[i].score)

    #play_control()

    # ROUND 4
    players = sorted(players, key=lambda x: (x.score, x.ranking), reverse=True)



    if has_played(players[0], players[1]) == False:
        match13 = Match(players[0], players[0].score, players[1], players[1].score)
    else:
        match13 = Match(players[0], players[0].score, players[2], players[2].score)
    if has_played(players[2], players[3]) == False:
        match14 = Match(players[2], players[2].score, players[3], players[3].score)
    else:
        match14 = Match(players[2], players[2].score, players[4], players[4].score)
    if has_played(players[4], players[5]) == False:
        match15 = Match(players[4], players[4].score, players[5], players[5].score)
    else:
        match15 = Match(players[4], players[4].score, players[6], players[6].score)
    if has_played(players[6], players[7]) == False:
        match16 = Match(players[6], players[6].score, players[7], players[7].score)
    else:
        match16 = Match(players[7], players[7].score, players[0], players[0].score)

    point_player0 = val[pos]
    players[0].score = players[0].score + float(point_player0)
    point_player1 = val[pos]
    players[1].score = players[1].score + point_player1
    point_player2 = val[pos]
    players[2].score = players[2].score + point_player2
    point_player3 = val[pos]
    players[3].score = players[3].score + point_player3
    point_player4 = val[pos]
    players[4].score = players[4].score + point_player4
    point_player5 = val[pos]
    players[5].score = players[5].score + point_player5
    point_player6 = val[pos]
    players[6].score = players[6].score + point_player6
    point_player7 = val[pos]
    players[7].score = players[7].score + point_player7

    match13 = Match(players[0], point_player1, players[4], point_player5)
    match14 = Match(players[1], point_player2, players[5], point_player6)
    match15 = Match(players[2], point_player3, players[6], point_player7)
    match16 = Match(players[3], point_player4, players[7], point_player8)

    round4_matchs = [match13, match14, match15, match16]
    round4 = Round(match_instance=round3_matchs, round_name="Round4",
                   start_date=View.round1_start_date, start_time=View.round1_start_time,
                   end_date=View.round1_end_date, end_time=View.round1_end_time
                   )
    tournament_instance.rounds.append(round4)
    round_list.append(round4)

    #play_control()
    #exit()

    print(has_played(players[0], players[4]))
    print(has_played(players[2], players[3]))
    print(has_played(players[4], players[5]))
    print(has_played(players[6], players[7]))




    # Result Reader
    #i = -1
    #for player in players:
    #   i += 1
    #    print(players[i].first_name)
    #    print(players[i].ranking)
    #    print(players[i].score)

    # Round 4 Control
    #print(has_played(players[0], players[1]))
    #print(has_played(players[2], players[3]))
    #print(has_played(players[4], players[5]))
    #print(has_played(players[6], players[7]))