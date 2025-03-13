class CleanGameLogs:
    def __init__(self, df): # pass df result from get_game_logs
        df.columns = [col.lower() for col in df.columns]
        self.raw_df = df.fillna(0) # fill null with zero (mostly for pct fields)
       
        self.player_box()
        self.player_shooting()
        self.team_box()
        self.team_shooting()
        self.game()
        
    
        
        
    def player_box(self):
        self.player_box_df = self.raw_df[['game_id', 'player_id', 'team_id', 'min', 'pts', 'ast',
                                                     'reb', 'stl', 'blk', 'oreb', 'dreb', 'tov', 'pf']]
    
    def player_shooting(self):
        self.player_shooting_df = self.raw_df[['game_id', 'player_id', 'team_id', 'fgm', 'fga',
        'fg3m', 'fg3a', 'ftm', 'fta', 'fg_pct', 'fg3_pct', 'ft_pct']]
        
    def team_box(self):
        self.team_box_df = self.raw_df[['game_id', 'team_id', 'team_abbreviation', 'min', 'pts', 'ast', 'reb', 'stl', 'blk', 
                                        'oreb', 'dreb', 'tov', 'pf']].groupby(['game_id', 'team_id', 'team_abbreviation']).sum().reset_index()
        
    def team_shooting(self):
        team_shots = (self.raw_df[['game_id', 'team_id', 'team_abbreviation', 'fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta']]
                      .groupby(['game_id', 'team_id', 'team_abbreviation'])).sum().reset_index()                                        
                                        
        team_eff = (self.raw_df[['game_id', 'team_id', 'team_abbreviation', 'fg_pct', 'fg3_pct', 'ft_pct']]
                    .groupby(['game_id', 'team_id', 'team_abbreviation']).mean().round(2).reset_index())
        
        self.team_shooting_df = team_shots.merge(team_eff, on=['game_id', 'team_id', 'team_abbreviation'], how='left')
        
    def get_final_scores(self):
        
        final_scores = self.team_box_df.pivot(index='game_id', columns='team_abbreviation', values='pts')
        
        def format_score(row):
            teams = list(row.dropna().index)  # Get team abbreviations
            scores = list(row.dropna().values)  # Get corresponding scores
            if len(teams) == 2:
                return f"{teams[0]} {int(scores[0])} - {int(scores[1])} {teams[1]}"
            return None

        final_scores['final_score'] = final_scores.apply(format_score, axis=1)
        final_scores = final_scores[['final_score']].reset_index()
        self.game_df = self.game_df.merge(final_scores, on='game_id', how='left')
        
    def get_ot_ind(self):
        game_minutes = self.team_box_df.groupby('game_id')['min'].sum().reset_index()
        game_minutes['ot_ind'] = (game_minutes['min'] > 500).astype(int)
        self.game_df = self.game_df.merge(game_minutes[['game_id', 'ot_ind']], on='game_id', how='left')
        
    def game(self):
        self.game_df = self.raw_df[['game_id', 'season_id', 'game_date', 'matchup']].drop_duplicates()
        self.get_final_scores()
        self.get_ot_ind()
        self.game_df['game_type'] = self.game_df['season_id'].astype(str).str[0].astype(int)
        drop_char = '@'
        drop_rows = self.game_df[self.game_df['matchup'].str.contains(drop_char, na=False)].index
        self.game_df = self.game_df.drop(drop_rows)
        
        #self.team_shooting_df 
def clean_game_logs_old(df):
    # need to create lists of tuples of values to insert into tables
    fields = []
    
    # TODO - add logic for mins > 240 indicaates OT
    game_data = list(df[['game_id', 'matchup', 'game_date']])
    fields.append(game_data)
    # TODO - produce final_score and ot_ind (sum mins > 480) fields
    
    team_data = list(df[['game_id', 'team_id', 'matchup', 'wl']])
    fields.append(team_data)
    
    player_box = df[[
        'game_id', 'player_id', 'team_id', 'min', 'pts', 'ast', # note min is mins in db
        'reb', 'stl', 'blk', 'oreb', 'dreb', 'tov', 'pf'
    ]]
    fields.append(player_box)
    print(player_box)
    
    player_shooting = df[[
        'game_id', 'player_id', 'team_id', 'fgm', 'fga',
        'fg3m', 'fg3a', 'ftm', 'fta', 'fg_pct', 'fg3_pct', 'ft_pct'
    ]]    
    return fields
