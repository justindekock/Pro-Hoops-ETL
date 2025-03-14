from datetime import datetime, timedelta
from fetch.call_nba_api import get_game_logs
from database.dml import insert_into

game_date =((datetime.today()) - timedelta(6)).strftime('%m/%d/%Y')
#print(game_date)

# returns a list of lists of tuples - each will contain the values to pass to insert into db tables
game_logs = get_game_logs(game_date)
# #print(game_logs.team_box_df)
print(game_logs.game_df)

# values = [(1001,'abc'), (1002,'abc'), (1003,'bch'), (1004,'abc'), (1005,'xyc'), (1006,'xyz')]
# insert_into('game', ['game_id', 'matchup',], values)
