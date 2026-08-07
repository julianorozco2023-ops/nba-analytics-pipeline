#Loaded into PostgreSQL. Raw data

import pandas as pd
from sqlalchemy import create_engine, text

#postgresql - type of database I'm connecting to
#psycopg2 - the driver being used to make that connection the library we installed that lets Python talk to PostgreSQL
#localhost - this means the database is running on my machine, not a remote server
#nba_pipeline - name of a specific database to connect to
engine = create_engine("postgresql+psycopg2://localhost/nba_pipeline")

#Drops 3 views, replace the 3 raw tables with fresh data, dbt runs and recreates the 3 views on top of the data
#Opens a connection to my database and calls it conn, same idea as engine
#It's the active bridge to postgreSQL. with is used here so the connection closes when the block finishes
with engine.connect() as conn:
#Drops the top_scorers view from the database before reloading the data
#DROP VIEW IF EXISTS - delete this view if it exists, don't error if it doesn't
#CASCADE - also drop anything that depends on it
#necessary because when load.py tries to replace the player_stats table with if_exists = replace, postegreSQL refuses since top_scorers is built on top of it
#Dropping the views first removes that dependency so the tables can be replaced freely
    conn.execute(text("DROP VIEW IF EXISTS top_scorers CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS team_records CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS team_game_logs CASCADE"))
#Confirms and saves the changes to the database, necessary or drops wouldn't take effect
    conn.commit()

#Reading all csv's
#Have to use the full path because it runs from its own working directory somewhere else on the machine
#it tells python exactly where the file is regardless of where the file is being run from
player_stats = pd.read_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/player_stats.csv")
standings = pd.read_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/standings.csv")
game_logs = pd.read_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/game_logs.csv")

#.to_sql - allows csv to be queried
#name - it creates this name, not in correlation to the previous names
#engine - it tells .to_sql which database to load the data into. Without it pandas wouldn't know where to send the data
#if_exists = "replace" - replaces the table if one with the same name already exists
player_stats.to_sql("player_stats", engine, if_exists="replace", index=False)
standings.to_sql("standings", engine, if_exists="replace", index=False)
game_logs.to_sql("game_logs", engine, if_exists="replace", index=False)

print("Done! All 3 tables loaded into nba_pipeline.")