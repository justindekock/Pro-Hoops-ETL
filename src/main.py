from datetime import datetime, timedelta
from fetch.call_nba_api import get_game_logs
from database.dml import insert_into

game_date =((datetime.today()) - timedelta(6)).strftime('%m/%d/%Y')
print(game_date)

# returns a list of lists of tuples - each will contain the values to pass to insert into db tables
game_logs = get_game_logs(game_date)
#print(game_logs.team_box_df)
print(game_logs.game_df)

