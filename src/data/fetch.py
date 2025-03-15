from time import sleep
from datetime import datetime, timedelta
from nba_api.stats.endpoints import leaguegamefinder
from data.clean import CleanGameLogs
from database.dml import separate_dfs, insert_into_tables
from log_config.logs import get_logger

logger = get_logger(__name__)

# TODO - function to fetch all active players everyday

def get_game_logs(game_date):
    retry_count = 0
    while retry_count < 3:
        try:
            game_logs_df = leaguegamefinder.LeagueGameFinder(
            player_or_team_abbreviation='P',
            league_id_nullable='00', # specifies NBA only
            date_from_nullable=game_date,
            date_to_nullable=game_date
            ).get_data_frames()[0]
            
            logger.info(f'Fetched {game_logs_df.shape[0]} game logs from {game_date}')
            
            return CleanGameLogs(game_logs_df)

        except Exception as e:
            print(e)
            retry_count += 1
            return None
        
def run_many_days(days=1): # will fetch data for and insert into tables for the number of days passed
    game_date_many = ((datetime.today()) - timedelta(1))
    for i in range(days):
        game_date = (game_date_many - timedelta(i)).strftime('%m/%d/%Y')
        game_logs = get_game_logs(game_date) 

        insert_lists = separate_dfs(game_logs.clean_logs)
        insert_into_tables(game_logs.tables, insert_lists)
        
        sleep(3)