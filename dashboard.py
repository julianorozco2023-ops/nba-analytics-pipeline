import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://localhost/nba_pipeline")

st.title("NBA Analytics Dashboard")

st.header("Top 25 Scorers")
top_scorers = pd.read_sql("select * from top_scorers", engine)
st.dataframe(top_scorers)

st.header("Team Records")
team_records = pd.read_sql("select * from team_records", engine)
st.dataframe(team_records)

st.header("Team Game Logs")
team_game_logs = pd.read_sql("select * from team_game_logs", engine)
st.dataframe(team_game_logs)
