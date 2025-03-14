import inspect
from nba_api.stats.endpoints import leaguegamefinder
from data.clean import CleanGameLogs

# TODO - function to fetch all active players everyday

def get_game_logs(game_date):
    game_logs =[]
    retry_count = 0
    while retry_count < 3:
        try:
            game_logs_df = leaguegamefinder.LeagueGameFinder(
            player_or_team_abbreviation='P',
            league_id_nullable='00', # specifies NBA only
            date_from_nullable=game_date,
            date_to_nullable=game_date
            ).get_data_frames()[0]
        
            clean_game_logs = CleanGameLogs(game_logs_df)
            methods = inspect.getmembers(clean_game_logs, predicate=inspect.ismethod)
            tables = []

            methods_to_exclude = ['__init__', 'get_final_scores', 'get_ot_ind']
            for method in methods:
                if method[0] in methods_to_exclude:
                    pass
                else:
                    tables.append(method[0])      
            
            print(tables)    
            
            return clean_game_logs.clean_dfs

        except Exception as e:
            print(e)
            retry_count += 1
            return None