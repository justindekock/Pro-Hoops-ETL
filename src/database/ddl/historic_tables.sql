/*CREATING DATABASE TABLES*/
use nba_historic;

create table if not exists season (
    season_id int not null,
    season varchar(13), 
    season_desc varchar(30),
    primary key (season_id)
);

create table if not exists game_type (
    game_type tinyint not null,
    game_type_desc varchar(50),
    primary key (game_type)
);

create table if not exists game (
    game_id int,
    season_id int, 
    game_date date, 
    matchup varchar(12), 
    final_score varchar(18), 
    ot_ind tinyint,
    game_type tinyint,
    primary key (game_id)
); 

create table if not exists all_teams (
    team_id int not null,
    team varchar(3) not null,
    team_name varchar(50),
    primary key (team_id)
);

create table if not exists all_players (
    player_id int not null,
    player_name varchar(255),
    team_id int not null,
    primary key (player_id),
    foreign key (team_id) references all_teams (team_id)
);

create table if not exists team_gamelog (
    game_id int not null,
    team_id int not null, 
    win_ind tinyint,
    home_ind tinyint, 
    primary key (game_id, team_id),
    foreign key (game_id) references game (game_id),
    foreign key (team_id) references all_teams (team_id)
);

create table if not exists player_box (
    game_id int not null, 
    team_id int not null,
    player_id int not null,
    mins tinyint,
    pts tinyint, 
    ast tinyint, 
    reb tinyint, 
    stl tinyint, 
    blk tinyint, 
    oreb tinyint,
    dreb tinyint,
    tov tinyint,
    pf tinyint,
    primary key (game_id, player_id),
    foreign key (game_id) references game (game_id),
    foreign key (team_id) references all_teams (team_id),
    foreign key (player_id) references all_players (player_id)
);

create table if not exists player_shooting (
    game_id int not null, 
    team_id int not null,
    player_id int not null,
    fgm tinyint, 
    fga tinyint,
    fg3m tinyint, 
    fg3a tinyint, 
    ftm tinyint,
    fta tinyint,
    fg_pct decimal(10,2),
    fg3_pct decimal(10,2),
    ft_pct decimal(10,2),
    primary key (game_id, player_id),
    foreign key (game_id) references game (game_id),
    foreign key (team_id) references all_teams (team_id),
    foreign key (player_id) references all_players (player_id)
);

create table if not exists team_box (
    game_id int not null, 
    team_id int not null,
    mins tinyint,
    pts tinyint, 
    ast tinyint, 
    reb tinyint, 
    stl tinyint, 
    blk tinyint, 
    oreb tinyint,
    dreb tinyint,
    tov tinyint,
    pf tinyint,
    primary key (game_id, team_id),
    foreign key (game_id) references game (game_id),
    foreign key (team_id) references all_teams (team_id)
);

create table if not exists team_shooting (
    game_id int not null, 
    team_id int not null,
    fgm tinyint, 
    fga tinyint,
    fg3m tinyint, 
    fg3a tinyint, 
    ftm tinyint,
    fta tinyint,
    fg_pct decimal(10,2),
    fg3_pct decimal(10,2),
    ft_pct decimal(10,2),
    primary key (game_id, team_id),
    foreign key (team_id) references all_teams (team_id)
);

create table if not exists playbyplay (
    game_id int not null,
    act_id smallint not null, 
    team_id int,
    player_id int,
    quarter tinyint,
    clock varchar(20),
    pts_total smallint, 
    score_h smallint,
    score_a smallint, 
    fg_ind boolean,
    shot_val tinyint, 
    shot_result boolean,
    act_type varchar(50),
    sub_type varchar(50),
    play_desc varchar(255),
    shot_dist tinyint,
    legacy_x smallint,
    legacy_y smallint, 
    vid_avail boolean,
    primary key (game_id, act_id),
    foreign key (team_id) references all_teams (team_id),
    foreign key (player_id) references all_players (player_id),
    foreign key (game_id) references game (game_id)
);

insert into all_teams (team_id, team, team_name) values (0, "NAT", "Playbyplay Placeholder");

insert into all_players (player_id, player_name, team_id) values (0, "Playbyplay Placeholder", 0);