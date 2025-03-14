from time import sleep
import inspect
from datetime import datetime, timedelta
from fetch.call_nba_api import get_game_logs
from database.dml import insert_into
from data.clean import df_to_insert_lists

game_date = ((datetime.today()) - timedelta(1)).strftime('%m/%d/%Y')
game_logs_dfs = get_game_logs(game_date)
print(len(game_logs_dfs))



# for df in game_logs_dfs:
#     flds_vals = df_to_insert_lists(df)
    #print(flds_vals)
    #insert_into(table=, fields=insert_lists[0], values=insert_lists[1])


def run_many_days(days, table):
    game_date_many = ((datetime.today()) - timedelta(1))
    for i in range(days):
        game_date_str = (game_date_many - timedelta(i)).strftime('%m/%d/%Y')
        print(game_date_str)
        game_logs = get_game_logs(game_date_str)
        insert_lists = df_to_insert_lists(game_logs[2])
        insert_into(table=table, fields=insert_lists[0], values=insert_lists[1])
        sleep(3)
        
run_many_days(20, 'player_box')
        
        
#run_many_days(1, 'active_players')


        # insert_into(table='active_players', fields=active_players[0], values=active_players[1])
        
        #insert_into(table='game', fields=insert_lists[0], values=insert_lists[1])
        #insert_into(table='active_teams', fields=active_teams[0], values=active_teams[1])

#print(game_date)

# returns a list of lists of tuples - each will contain the values to pass to insert into db tables
# game_logs = get_game_logs(game_date)
# insert_lists = df_to_insert_lists(game_logs.game_df)
# active_players = df_to_insert_lists(game_logs.active_players_df)
# active_teams = df_to_insert_lists(game_logs.active_teams_df)



#insert_player_box
#insert_into(table='game', fields=insert_lists[0], values=insert_lists[1])
#insert_into(table='active_players', fields=active_players[0], values=active_players[1])
#insert_into(table='active_teams', fields=active_teams[0], values=active_teams[1])

#print(game_logs.game_df.values.to_list())

# #print(game_logs.team_box_df)
#print(game_logs.game_df)

# values = [(1001,'abc'), (1002,'abc'), (1003,'bch'), (1004,'abc'), (1005,'xyc'), (1006,'xyz')]
# insert_into('game', ['game_id', 'matchup',], values)
