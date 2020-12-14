import pandas as pd
import datetime
from datetime import date
from sportsreference.nba.boxscore import Boxscore
from sportsreference.nba.boxscore import Boxscores
from sportsreference.nba.teams import Teams
from sportsreference.nba.schedule import Schedule

def find_games_played(abbreviation):
    df1 = Schedule(abbreviation)
    counter = 0
    for game in df1:
        if (type(game.points_scored) == int):
            counter += 1
    return counter

#for the next game to be played
def find_avg_ppg_over_last_10(abbreviation):
    games_played = find_games_played(abbreviation)
    df2 = Schedule(abbreviation).dataframe
    df_onlylast10 = df2.iloc[(games_played - 10):games_played]
    return df_onlylast10.points_scored.mean()

def both_teams_avg_game_points_last_10(abbreviation1, abbreviation2):
    estimate = total_game_points_scored_over_last_10(abbreviation1) + total_game_points_scored_over_last_10(abbreviation2)
    final_estimate = estimate / 2
    return final_estimate

def total_game_points_scored_over_previous_10(abbreviation, game, year):
    game_number = game
    df2 = Schedule(abbreviation, year).dataframe
    df_onlylast10 = df2.iloc[(game_number - 11):(game_number-1)]
    return df_onlylast10.points_allowed.mean() + df_onlylast10.points_scored.mean()


def both_teams_avg_game_points_previous_10(abbreviation1, abbreviation2, rboxscore_index):
    sched1 = Schedule(abbreviation1)
    sched2 = Schedule(abbreviation2)
    index_to_match = rboxscore_index
    game1 = 0
    game2 = 0
    for game in sched1:
        if index_to_match == game.boxscore_index:
            game1 = game.game
    for game in sched2:
        if index_to_match == game.boxscore_index:
            game2 = game.game
    estimate = total_game_points_scored_over_previous_10(abbreviation1, game1) + total_game_points_scored_over_previous_10(abbreviation2, game2)
    final_estimate = estimate / 2
    return final_estimate

def find_game_points(abbreviation, boxscore_index):
    sched1 = Schedule(abbreviation)
    for game in sched1:
        if boxscore_index == game.boxscore_index:
            total_score = game.points_scored + game.points_allowed
            return total_score
    return 0


def interface():
    teamname1 = input("Please enter first team name abbreviation:\n")
    teamname2 = input("Please enter second team name abbreviation:\n")
    average_pointage = both_teams_avg_game_points_last_10(teamname1, teamname2)
    print("The average points scored in the last 10 games for both teams is ",round(average_pointage,2))

def schedule_for_the_day(mydate):
    for team in Teams():
        team_schedule = Schedule(team.abbreviation)
        for game in team_schedule:
            if (game.datetime.date() == mydate):
                if (game.location == "Away"):
                    print(game.time)
                    print(team.abbreviation,"@ ",game.opponent_abbr)
                    expected_points = both_teams_avg_game_points_previous_10(team.abbreviation, game.opponent_abbr, game.boxscore_index)
                    real_expected_points = round(expected_points, 2)
                    print("The expected total points scored for this game is " + str(real_expected_points))
                    points_scored = find_game_points(team.abbreviation, game.boxscore_index)
                    print("The total points scored in this game was " + str(points_scored))
                    print()



def schedule_for_today():
    date_today = datetime.date.today()
    print("Today's date is " + str(date_today))
    print("Here are the games for today:")
    schedule_for_the_day(date_today)


def schedule_for_any_day():
    year = int(input("Please enter year number:\n"))
    month = int(input("Please enter month number:\n"))
    day = int(input("Please enter day number:\n"))
    date = datetime.date(year, month, day)
    schedule_for_the_day(date)

def date_generators():
    a = datetime.datetime.today()
    numdays = 75
    dateList = []
    for x in range (0, numdays):
        season_start_day = datetime.date(2019, 10, 22)
        dateList = [season_start_day + datetime.timedelta(days=x) for x in range(numdays)]
    return dateList

def predicted_point_total_all_games_this_season():
    dateList = date_generators()
    dateList = dateList[50:]
    for date in dateList:
        print("Here are the games for " + str(date) + ":")
        print()
        predict(games_for_the_day(date), date.year)

def games_for_the_day(date):
    games = Boxscores(date)
    date_string = str(date.month) + '-' + str(date.day) + '-' + str(date.year)
    list1 = games.games[date_string]
    print(list1)
    boxscores = []
    print("Here are the games for " + str(date) + ":")
    print()
    for game in list1:
        away_abbr = game['away_abbr']
        home_abbr = game['home_abbr']
        print(game.keys())
        break
        index = game['boxscore']
        total_score = game['away_score'] + game['home_score']
        prediction = round(both_teams_avg_game_points_previous_10(away_abbr, home_abbr, index), 2)
        print(away_abbr + " @ " + home_abbr)
        print("Predicted Score: " + str(prediction))
        print("Actual Score: " + str(total_score))
        print()

def predict(boxscores, year):
    for boxscore in boxscores:
        box1 = Boxscore(boxscore)
        home_games = box1.home_wins + box1.home_losses
        away_games = box1.away_wins + box1.away_losses
        if box1.home_points > box1.away_points:
            away_abbrev = box1.losing_abbr
            home_abbrev = box1.winning_abbr
        else:
            away_abbrev = box1.winning_abbr
            home_abbrev = box1.losing_abbr
        estimate = round(total_game_points_scored_over_previous_10(away_abbrev, away_games, year) + total_game_points_scored_over_previous_10(home_abbrev, home_games, year), 2)
        final_estimate = str(estimate / 2)
        print(away_abbrev + " @ " + home_abbrev)
        print("Predicted Score: " + final_estimate)
        print("Actual Score: " + str((box1.home_points + box1.away_points)))
        print()


def games_for_the_day(date1):
    games = Boxscores(date1)
    date_string = str(date1.month) + '-' + str(date1.day) + '-' + str(date1.year)
    list1 = games.games[date_string]
    boxscores = []
    for game in list1:
        index = game['boxscore']
        boxscores.append(index)
    return boxscores


def main():
    
    predicted_point_total_all_games_this_season()

main()

