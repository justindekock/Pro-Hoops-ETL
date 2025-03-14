class CleanGameLogs:
    def __init__(self, df): # pass df result from get_game_logs
        # clean the raw data
        df.columns = [col.lower() for col in df.columns]
        self.raw_df = df.fillna(0) # fill null with zero (mostly for pct fields)
        self.raw_df = df.rename(columns={'team_abbreviation': 'team', 'min': 'mins'})
        
        self.raw_df.to_csv('raw.csv', index=False)
        
        self.clean_dfs = []
        
        self.clean_dfs.append(self.active_players())
        self.clean_dfs.append(self.active_teams())
        self.clean_dfs.append(self.player_box())
        self.clean_dfs.append(self.player_shooting())
        self.clean_dfs.append(self.team_box())
        self.clean_dfs.append(self.team_shooting())
        self.clean_dfs.append(self.game())
        
    # create subset dfs for each table 
    def active_players(self):
        self.active_players_df = self.raw_df[['player_id', 'player_name', 'team_id']]
        #self.players_table
        return self.active_players_df
        
    def active_teams(self):
        self.active_teams_df = self.raw_df[['team_id', 'team', 'team_name']]
        return self.active_teams_df
    
    def player_box(self):
        self.player_box_df = self.raw_df[['game_id', 'player_id', 'team_id', 
                                          'mins', 'pts', 'ast', 'reb', 'stl', 'blk', 'oreb', 'dreb', 'tov', 'pf']]
        return self.player_box_df
    
    def player_shooting(self):
        self.player_shooting_df = self.raw_df[['game_id', 'player_id', 'team_id', 'fgm', 'fga',
            'fg3m', 'fg3a', 'ftm', 'fta', 'fg_pct', 'fg3_pct', 'ft_pct']]
        return self.player_shooting_df
        
    def team_box(self):
        self.team_box_df = self.raw_df[['game_id', 'team_id', 'team', 'mins', 'pts', 'ast', 'reb',
            'stl', 'blk', 'oreb', 'dreb', 'tov', 'pf']].groupby(['game_id', 'team_id', 'team']).sum().reset_index()
        return self.team_box_df
    
    def team_shooting(self):
        team_shots = (self.raw_df[['game_id', 'team_id', 'team', 'fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta']]
                      .groupby(['game_id', 'team_id', 'team'])).sum().reset_index()                                        
                                        
        team_eff = (self.raw_df[['game_id', 'team_id', 'team', 'fg_pct', 'fg3_pct', 'ft_pct']]
                    .groupby(['game_id', 'team_id', 'team']).mean().round(2).reset_index())
        
        self.team_shooting_df = team_shots.merge(team_eff, on=['game_id', 'team_id', 'team'], how='left')
        return self.team_shooting_df
        
    # functions for game table (final score, overtime)
    def get_final_scores(self):
        final_scores = self.team_box_df.pivot(index='game_id', columns='team', values='pts')
        
        def format_score(row): # pass to each row with apply function
            teams = list(row.dropna().index)
            scores = list(row.dropna().values)
            if len(teams) == 2: # eg 'DAL 110 - 105 BOS
                return f"{teams[0]} {int(scores[0])} - {int(scores[1])} {teams[1]}"
            return None

        final_scores['final_score'] = final_scores.apply(format_score, axis=1)
        final_scores = final_scores[['final_score']].reset_index()
        self.game_df = self.game_df.merge(final_scores, on='game_id', how='left')
        
    def get_ot_ind(self):
         # if the total sum of points is > 480, the game went to OT 
        game_minutes = self.team_box_df.groupby('game_id')['mins'].sum().reset_index()
        
        # some non-ot games end up with +- 2-3 from 480, but ot game will have at least 530
        game_minutes['ot_ind'] = (game_minutes['mins'] > 500).astype(int)
        self.game_df = self.game_df.merge(game_minutes[['game_id', 'ot_ind']], on='game_id', how='left')
        
    def game(self):
        self.game_df = self.raw_df[['game_id', 'season_id', 'game_date', 'matchup']].drop_duplicates()
        
        self.get_final_scores()
        self.get_ot_ind()
        
        # derive game type from first digit of season_id - 2 = regular season, 4 is post season
        self.game_df['game_type'] = self.game_df['season_id'].astype(str).str[0].astype(int)
        
        drop_char = '@'
        drop_rows = self.game_df[self.game_df['matchup'].str.contains(drop_char, na=False)].index
        self.game_df = self.game_df.drop(drop_rows)
        return self.game_df
    

# function to convert df to a list of fields and list of values    
def df_to_insert_lists(df):
    fields = []
    vals = []
    #print(df.columns[0])
    
    fields_np = df.columns
    for field in fields_np:
        fields.append(field)
    
    vals_np = df.to_numpy()
    for val in vals_np:
        val = list(val)
        vals.append(val)
    
    #print(vals)
    return [fields, vals]