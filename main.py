#Extracted raw data from the NBA API

#imports 3 API endpoints to fetch data
from nba_api.stats.endpoints import leagueleaders, leaguestandingsv3, teamgamelog
#imports the static list of all 30 NBA teams
from nba_api.stats.static import teams
import pandas as pd, time
#use this if using Path for file paths, not in this case
from pathlib import Path


#Fetches the list of all 30 teams as dictionaries
all_teams = teams.get_teams()

#API Request
#season = SEASON - which season to pull
#stat_category_abbreviation = 'PTS' - sort players by points. Could be changed to "REB" for rebounds or "AST" for assists
#per_mode48 = "PerGame" - return stats averaged per game rather than season totals
#calling LeagueLeaders(...) sends HTTP request to NBA's stats site and stores response in the leaders variable
leaders = leagueleaders.LeagueLeaders(season ="2024-25", stat_category_abbreviation="PTS", per_mode48="PerGame")

#Convert the response to a table (DataFrame)
#.get_data_frames()[0] means give me the first table from the API response
#This is what pulls the 231 players in order of top scorers of the league in the season in order
df = leaders.get_data_frames()[0]

#Save to a csv file
#index = false just removes 0, 1, 2, ... from left hand side
#data/ - a folder called data
#raw/ - a subfolder inside data called raw
#player_stats.csv - the file name
#a file path - tells python where to save the file
df.to_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/player_stats.csv", index = False)

#Rate-limiter
#NBA's API will block me if too many requests are sent too fast, this gives a pause between requests
time.sleep(0.6)

#collect each team's games
all_logs = []
for team in all_teams:
    #Fetches the teams game log using their ID from the dictionary
    log = teamgamelog.TeamGameLog(team_id = team["id"],
    season = "2024-25")
    #Converts the response to a dataframe and returns the first table from the API call with all the game logs data for all teams
    df = log.get_data_frames()[0]
    #Adds a new column with the team's full name so you know which team each row belongs to after combining
    df["TEAM_NAME"] = team["full_name"]
    #Adds the dataframe to the list, the pauses before the next team
    all_logs.append(df)
    time.sleep(0.6)

#stack all 30 dataframes on top of each other into one big table. Gives 2,460 rows
combined = pd.concat(all_logs, ignore_index=True)

#Save game logs
combined.to_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/game_logs.csv", index = False)

#Fetch and save standings
#Make the api request -> store in standings
#Pull the table out -> store in df
#Save to csv
standings = leaguestandingsv3.LeagueStandingsV3(season="2024-25")
df = standings.get_data_frames()[0]
df.to_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/standings.csv", index = False)


