from nba_api.stats.endpoints import leaguegamefinder

# TODO - function to fetch all active players everyday

def clean_game_logs(df):
    # return list of list of tuples
    fields = []
    
    
    df.columns = [col.lower() for col in df.columns]
    
    game_data = list(df[['game_id', 'matchup', 'game_date']])
    fields.append(game_data)
    # TODO - produce final_score and ot_ind (sum mins > 480) fields
    
    team_data = list(df[['game_id', 'team_id', 'matchup', 'wl']])
    fields.append(team_data)
    
    player_box = list(df[[
        'game_id', 'player_id', 'team_id', 'pts', 'ast',
        'reb', 'stl', 'blk', 'oreb', 'dreb', 'tov', 'pf'
    ]])
    fields.append(player_box)
    
    player_shooting = list(df[[
        'game_id', 'player_id', 'team_id', 'fgm', 'fga',
        'fg3m', 'fg3a', 'ftm', 'fta', 'fg_pct', 'fg3_pct', 'ft_pct'
    ]])
    fields.append(player_shooting)
    
    return fields
    

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
            
            # print(game_logs_df.columns)
            # changed this to fields - need to then pass back to df to get the values
            game_logs = clean_game_logs(game_logs_df)
            break

        except Exception as e:
            print(e)
            retry_count += 1

    return game_logs



# game_logs = get_game_logs('3/9/2025')
# print(game_logs)
