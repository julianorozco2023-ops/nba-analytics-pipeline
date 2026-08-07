select "TeamCity", "TeamName", "Conference", "WINS",
       "LOSSES", "WinPCT", "HOME", "ROAD", "L10"
from {{ source('public', 'standings') }}
order by "WinPCT" desc