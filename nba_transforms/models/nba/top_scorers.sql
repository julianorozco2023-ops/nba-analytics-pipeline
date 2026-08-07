SELECT
    "PLAYER",
    "TEAM",
    "GP",
    "PTS",
    "AST",
    "REB",
    "EFF"
FROM {{ source('public', 'player_stats') }}
ORDER BY "PTS" DESC
LIMIT 25