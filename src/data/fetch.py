from time import sleep
from datetime import datetime, timedelta
from nba_api.stats.endpoints import leaguegamefinder, playbyplayv3
from data.clean import CleanGameLogs, CleanPlaybyPlay
from database.dml import separate_dfs, insert_into_tables, insert_pbp
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
            
            game_logs_df.to_csv('raw.csv')
            
            if game_logs_df.shape[0] > 0:
                logger.info(f'Fetched {game_logs_df.shape[0]} game logs from {game_date}')    
                return CleanGameLogs(game_logs_df)
            
            else: 
                logger.info(f'No games fetched for {game_date}')
                return None
            
        except Exception:
            logger.exception(f'Error fetching games for {game_date} after {retry_count} try(ies)')
            retry_count += 1
            sleep(10)
            
    return None

# TODO - write function to fetch play-by-play data
def get_playbyplay(game_ids): # accept list of game_ids from the game_logs fetched
    pbp_data = []
    for game_id in game_ids:
        delay = 10
        retry_count = 0
    
        while retry_count < 3:
            try: 
                logger.debug(f'Attempting play-by-play fetch for {game_id}')
                pbp_df = playbyplayv3.PlayByPlayV3(game_id).get_data_frames()[0]
                pbp_recs = pbp_df.shape[0]
                if pbp_recs > 0:
                    pbp_data.append(pbp_df)
                    logger.info(f'Play-by-play data ({pbp_recs} rows) successfully fetched for {game_id}')
                    break
  
            except Exception:
                logger.exception(f'Failed fetching play-by-play for {game_id}')

    return CleanPlaybyPlay(pbp_data)
    
def run_many_days(days=1): # will fetch data for and insert into tables for the number of days passed)
    game_date_many = ((datetime.today()) - timedelta(1))
    for i in range(days):
        game_date = (game_date_many - timedelta(i)).strftime('%m/%d/%Y')
        game_logs = get_game_logs(game_date) 
        
        if game_logs:
            try:
                insert_lists = separate_dfs(game_logs.clean_logs)
                insert_into_tables(game_logs.tables, insert_lists)
                logger.info(f'Game log ETL complete for {game_date} -- fetching play-by-play data')
                
                game_ids = game_logs.clean_logs[2]['game_id'].values
                if len(game_ids) > 0:
                    try:
                        playbyplay = get_playbyplay(game_ids) # returns list of clean dfs
                        pbp_inserts = separate_dfs(playbyplay.clean_pbp_dfs)
                        try:
                            print(pbp_inserts[0])
                            insert_pbp('playbyplay', pbp_inserts)    
                            logger.info('Succesfully inserted playbyplay data')
                        except Exception:
                            logger.exception('Error inserting play-by-play data')
                        
                    except Exception:
                        logger.exception('Error fetching play-by-play data')
                
            except Exception:
                logger.exception(f'Error inserting into database')
                
        else:
            logger.info(f'No game logs fetched for {game_date}')
        
        if (i % 50) == 0:
            delay = 60
        elif (i % 10) == 0:
            delay = 20
        else:
            delay = 3
            
        logger.debug(f'Delaying for {delay} seconds...')