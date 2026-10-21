import streamlit as st
import pandas as pd

from db import get_engine

engine = get_engine()

st.title("NBA Analytics Dashboard")

# Number rows from 1 so the top-ranked row shows as 1, not 0
st.header("Top 25 Scorers")
top_scorers = pd.read_sql("select * from top_scorers", engine)
top_scorers.index += 1
st.dataframe(top_scorers)

st.header("Team Records")
team_records = pd.read_sql("select * from team_records", engine)
team_records.index += 1
st.dataframe(team_records)

st.header("Team Game Logs")
team_game_logs = pd.read_sql("select * from team_game_logs", engine)
team_game_logs.index += 1
st.dataframe(team_game_logs)
