#Visual commands library
import streamlit as st
import pandas as pd
#Library to use create_engine to connect to a database
from sqlalchemy import create_engine

#Making the connection to the database and setting it to engine
engine = create_engine("postgresql+psycopg2://localhost/nba_pipeline")

#Visual dashboard title
st.title("NBA Analytics Dashboard")

#Visual dashboard first header
st.header("Top 25 Scorers")
#Reads the team_records view and selects all the columns in said view and turns it into a dataframe stored in top_scorers (engine is to bridge to the database)
top_scorers = pd.read_sql("select * from top_scorers", engine)
#Creates a visual in the dashboard of all the data in the dataframe of top_scorers.
st.dataframe(top_scorers)

#Another header
st.header("Team Records")
team_records = pd.read_sql("select * from team_records", engine)
st.dataframe(team_records)

st.header("Team Game Logs")
team_game_logs = pd.read_sql("select * from team_game_logs", engine)
st.dataframe(team_game_logs)