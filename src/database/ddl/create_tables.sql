/*CREATING DATABASE TABLES*/
use prohoops;
create table if not exists game (
    game_id int,
    season_id int, 
    game_date date, /*YYYY-MM-DD*/
    matchup varchar(12), /*use home team's matchup*/
    final_score varchar(18), /*LAL 110 - 109 BOS*/
    ot_ind tinyint,
    game_type tinyint,
    primary key (game_id)
); 

create table if not exists active_teams (
    team_id int not null,
    team varchar(3) not null,
    team_name varchar(50),
    primary key (team_id)
);

create table if not exists active_players (
    player_id int not null,
    player_name varchar(255),
    team_id int not null,
    primary key (player_id),
    foreign key (team_id) references active_teams (team_id)
);

create table if not exists team_gamelog (
    game_id int not null,
    team_id int not null, 
    win_ind tinyint, /*1 is win*/
    home_ind tinyint, /*1 is home*/
    primary key (game_id, team_id),
    foreign key (game_id) references game (game_id),
    foreign key (team_id) references active_teams (team_id)
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
    foreign key (team_id) references active_teams (team_id),
    foreign key (player_id) references active_players (player_id)
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
    fgp decimal(10,2),
    fg3p decimal(10,2),
    ftp decimal(10,2),
    primary key (game_id, player_id),
    foreign key (game_id) references game (game_id),
    foreign key (team_id) references active_teams (team_id),
    foreign key (player_id) references active_players (player_id)
);

create table if not exists team_box (
    game_id int not null, 
    team_id int not null,
    mins tinyint, -- mins > 240 indicates overtime
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
    foreign key (team_id) references active_teams (team_id)
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
    fgp decimal(10,2),
    fg3p decimal(10,2),
    ftp decimal(10,2),
    primary key (game_id, team_id)
);

create table if not exists game_type (
    game_type tinyint not null,
    game_type_desc varchar(50),
    primary key (game_type)
);





/*insert into game_type values (1, 'Preseason'), (2, 'Regular Season'), (4, 'Playoffs') ;*/
/*
use prohoops;
drop table team_gamelog;
drop table game;
*/

