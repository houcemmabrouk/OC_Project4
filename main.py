import Controller
import Model
import View



if __name__ == '__main__':

    player1 = Model.Player(first_name=View.player1_first_name,
                           last_name=View.player1_last_name,
                           date_of_birth=View.player1_date_of_birth,
                           gender=View.player1_gender,
                           ranking=View.player1_ranking,
                           score=0
                           )
    player2 = Model.Player(first_name=View.player2_first_name,
                           last_name=View.player2_last_name,
                           date_of_birth=View.player2_date_of_birth,
                           gender=View.player2_gender,
                           ranking=View.player2_ranking,
                           score=0
                           )
    player3 = Model.Player(first_name=View.player3_first_name,
                           last_name=View.player3_last_name,
                           date_of_birth=View.player3_date_of_birth,
                           gender=View.player3_gender,
                           ranking=View.player3_ranking,
                           score=0
                           )
    player4 = Model.Player(first_name=View.player4_first_name,
                           last_name=View.player4_last_name,
                           date_of_birth=View.player4_date_of_birth,
                           gender=View.player4_gender,
                           ranking=View.player4_ranking,
                           score=0
                           )
    player5 = Model.Player(first_name=View.player5_first_name,
                           last_name=View.player5_last_name,
                           date_of_birth=View.player5_date_of_birth,
                           gender=View.player5_gender,
                           ranking=View.player5_ranking,
                           score=0
                           )
    player6 = Model.Player(first_name=View.player6_first_name,
                           last_name=View.player6_last_name,
                           date_of_birth=View.player6_date_of_birth,
                           gender=View.player6_gender,
                           ranking=View.player6_ranking,
                           score=0
                           )
    player7 = Model.Player(first_name=View.player7_first_name,
                           last_name=View.player7_last_name,
                           date_of_birth=View.player7_date_of_birth,
                           gender=View.player7_gender,
                           ranking=View.player7_ranking,
                           score=0
                           )
    player8 = Model.Player(first_name=View.player8_first_name,
                           last_name=View.player8_last_name,
                           date_of_birth=View.player8_date_of_birth,
                           gender=View.player8_gender,
                           ranking=View.player8_ranking,
                           score=0
                           )

    players_instance = [player1, player2, player3, player4, player5, player6, player7, player8]

    tournament_instance = Model.Tournament(name=View.tournament_name,
                                           place=View.tournament_place,
                                           date=View.tournament_date,
                                           number_of_rounds=4,
                                           rounds=[],
                                           players=players_instance,
                                           timing_type=View.tournament_timing_type,
                                           description=View.tournament_description,
                                           )

    player_w = player1
    player_b = player2

    match = Model.Match(player_white=player_w, score_white=0, player_black=player_b, score_black=0)
    match = ([player_w, 0], [player_b, 0])


    players_instance = sorted(players_instance, key=lambda x: x.ranking, reverse=True)
    players = {}
    i = 0
    for player in players_instance:
        i += 1
        players[i] = player

    print(players[1].ranking)

    # Match Result

    point_player1 = input("Enter score for " + players[1].first_name + " " + players[1].last_name)
    players[1].score = float(point_player1)
    point_player2 = 0.5
    players[2].score = float(point_player2)
    point_player3 = 1
    players[3].score = float(point_player3)
    point_player4 = 0.5
    players[4].score = float(point_player4)
    point_player5 = 0
    players[5].score = float(point_player5)
    point_player6 = 1
    players[6].score = float(point_player6)
    point_player7 = 0.5
    players[7].score = float(point_player7)
    point_player8 = 0.5
    players[8].score = float(point_player8)


    match1 = ([players[1], point_player1], [players[5], point_player5])
    match2 = ([players[2], point_player2], [players[6], point_player6])
    match3 = ([players[3], point_player3], [players[7], point_player7])
    match4 = ([players[4], point_player4], [players[8], point_player8])


    print(match4)

    match_instance = [match1, match2, match3, match4]
    round1 = Model.Round(match_instance=match_instance, round_name="Round1",
                         start_date=View.round1_start_date, start_time=View.round1_start_time,
                         end_date=View.round1_end_date, end_time=View.round1_end_time)

    players_instance = sorted(players_instance, key=lambda x: (x.score, x.ranking), reverse=True)

    players = {}
    i = 0
    for player in players_instance:
        i += 1
        players[i] = player
        print(player.score)
        print(player.ranking)

    print(match1)
    print(match2)
    print(match3)
    print(match4)
