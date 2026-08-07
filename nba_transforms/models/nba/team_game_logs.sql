select "TEAM_NAME", "GAME_DATE", "MATCHUP", "WL", "PTS",
       "FG_PCT", "FG3_PCT", "REB", "AST", "TOV"
from {{ source('public', 'game_logs') }}
order by "TEAM_NAME", "GAME_DATE" desc