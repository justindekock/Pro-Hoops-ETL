import pandas as pd
from log_config.logs import get_logger

logger = get_logger(__name__)

class CleanGameLogs:
    def __init__(self, df): # pass df result from get_game_logs
        logger.info(f'Cleaning and transforming {df.shape[0]} game logs for insert')

        self.raw_df = self.clean_global_df(df)
        
        # create subset dfs for each database table
        active_players_df = self.active_players(self.raw_df)
        active_teams_df = self.active_teams(self.raw_df)
        game_df = self.game(self.raw_df)
        player_box_df = self.player_box(self.raw_df)
        player_shooting_df = self.player_shooting(self.raw_df)
        team_box_df = self.team_box(self.raw_df)
        team_shooting_df = self.team_shooting(self.raw_df)
        team_gamelog_df = self.team_gamelog(self.raw_df)
        
        # add clean dfs to list
        self.clean_logs = []
        self.clean_logs.extend([active_players_df, active_teams_df, game_df, player_box_df,
                                player_shooting_df, team_box_df, team_shooting_df, team_gamelog_df])
        
        
         # TODO - find better way to get this list
        self.tables = ['active_players', 'active_teams', 'game', 'player_box', 'player_shooting', 'team_box',
                  'team_shooting', 'team_gamelog']
         
    
    # clean/rename columns in the raw df api response
    def clean_global_df(self, df):
        df.columns = [col.lower() for col in df.columns]
        raw_df = df.fillna(0) # fill null with zero (mostly for pct fields)
        raw_df = df.rename(columns={'team_abbreviation': 'team', 'min': 'mins'})
        return raw_df
 
    # create subset dfs for each table 
    def active_players(self, df):
        active_players_df = df[['player_id', 'player_name', 'team_id']]
        return active_players_df
        
    def active_teams(self, df):
        active_teams_df = df[['team_id', 'team', 'team_name']]
        return active_teams_df
    
    def game(self, df):
        def drop_away_matchups(df):
            # since the 12/14/2024 NBA cup game was at a neautral location, all matchup have '@' - replace for just the two games on that day
            df.loc[df['game_id'].isin(['0022401229', '0022401230']), 'matchup'] = df['matchup'].str.replace('@', 'vs.')
                
            drop_char = '@'
            drop_rows = df[df['matchup'].str.contains(drop_char, na=False)].index
            return df.drop(drop_rows)
        
        def get_ot_ind(df):
            df['ot_ind'] = (df['mins'] > 500).astype(int)
            return df.drop(['mins'], axis=1)
        
        def get_final_scores(df): # adds a formatted final score column
            final_scores = df.pivot(index='game_id', columns='team', values='pts')
            
            # returns string formatted score - pass with .apply to each row
            def format_score(row): # pass to each row with apply function
                teams = list(row.dropna().index)
                scores = list(row.dropna().values)
                if len(teams) == 2: # eg 'DAL 110 - 105 BOS
                    return f"{teams[0]} {int(scores[0])} - {int(scores[1])} {teams[1]}"
                return None

            # run the function to get the scores
            final_scores['final_score'] = final_scores.apply(format_score, axis=1)
            final_scores = final_scores[['final_score']].reset_index()
            
            # return final scores df merged with fd passed in
            return (df.merge(final_scores, on='game_id', how='left')
                    .drop(['team', 'pts'], axis=1).drop_duplicates())
        
        # ============================================================================================
        # first four cols - id, season, date, matchup
        game_df = drop_away_matchups(df[['game_id', 'season_id', 'game_date', 'matchup']].drop_duplicates())
        
        
        # get game type (first digit of season_id)
        game_df['game_type'] = game_df['season_id'].astype(str).str[0].astype(int)
        
        # overtime indicator 
        ot_df = get_ot_ind(df[['game_id', 'mins']].groupby('game_id').sum().reset_index())
        
        # final scores
        score_df = get_final_scores(
            df[['game_id', 'team', 'pts']].groupby(['game_id', 'team']).sum().reset_index())
        
        # merge all dfs together and return
        return pd.merge(pd.merge(game_df, ot_df, on='game_id'), score_df, on='game_id')
    
    def player_box(self, df):
        player_box_df = df[['game_id', 'player_id', 'team_id', 'mins', 'pts',
            'ast', 'reb', 'stl', 'blk', 'oreb', 'dreb', 'tov', 'pf']]
        return player_box_df
    
    def player_shooting(self, df):
        player_shooting_df = df[['game_id', 'player_id', 'team_id', 'fgm', 'fga',
            'fg3m', 'fg3a', 'ftm', 'fta', 'fg_pct', 'fg3_pct', 'ft_pct']]
        return player_shooting_df
        
    def team_box(self, df):
        team_box_df = (df[['game_id', 'team_id', 'mins', 'pts', 'ast', 'reb',
            'stl', 'blk', 'oreb', 'dreb', 'tov', 'pf']]
            .groupby(['game_id', 'team_id']).sum().reset_index())
        return team_box_df
    
    def team_shooting(self, df):
        team_shots = (df[['game_id', 'team_id', 'fgm', 'fga', 
            'fg3m', 'fg3a', 'ftm', 'fta']].groupby(
                ['game_id', 'team_id'])).sum().reset_index()                                        
                                        
        team_eff = (df[['game_id', 'team_id', 'fg_pct', 'fg3_pct', 'ft_pct']]
                    .groupby(['game_id', 'team_id']).mean().round(2).reset_index())
        
        team_shooting_df = team_shots.merge(
            team_eff, on=['game_id', 'team_id'], how='left')
        return team_shooting_df
    
    def team_gamelog(self, df):
        def get_home_ind(df): # returns 0 if matchup contains '@'
            df['home_ind'] = (df['matchup'].apply(lambda x: 0 if '@' in x else 1))
            return df
        
        def get_win_ind(df): # pivot used to compare scores, returns 1 if score is max 
            scores_df = df.pivot(index='game_id', columns='team_id', values='pts')
            df['win_ind'] = df.apply(lambda row: 
                int(row['pts'] == scores_df.loc[row['game_id']].max()), axis=1)
            return df
        
        working_df = (df[['game_id', 'team_id', 'matchup', 'pts']]
                           .groupby(['game_id', 'team_id', 'matchup'])).sum().reset_index()
        
        # add indicator cols
        working_df = get_win_ind(working_df)
        working_df = get_home_ind(working_df)
        
        # drop unneeded cols
        team_gamelog_df = working_df.drop(['matchup', 'pts'], axis=1)
        return team_gamelog_df