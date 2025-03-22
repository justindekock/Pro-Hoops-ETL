create or replace view pt as 
    select a.player_name, b.team_name 
    from active_players a 
    inner join active_teams b on a.team_id = b.team_id;

create or replace view pt_count as 
    select a.player_name, count(a.team_id) as teams
    from active_players a 
    group by a.player_name;

create or replace view trade_count as
    select count(*) as traded_players
    from pt_count
    where teams > 1;

create or replace view top_scorers as
    select 
        a.player_id,
        b.player_name,
        c.team_name,
        sum(a.pts) as total_points, 
        sum(a.ast) as total_ast,
        sum(a.reb) as total_reb,
        sum(a.stl) as total_stl,
        sum(a.blk) as total_blk

    from player_box a 
     inner join active_players b on a.player_id = b.player_id
     inner join active_teams c on b.team_id = c.team_id

    group by a.player_id, b.player_name, c.team_name

    order by total_points desc;

select distinct a.game_date
from game a
inner join team_gamelog b on a.game_id = b.game_id
inner join active_teams c on b.team_id = c.team_id
where c.team = 'OKC'
order by a.game_date;

create view pbp_detail as 
    select 
        a.game_id,
        a.act_id,
        a.quarter,
        a.clock,
        c.team,
        b.player_name,
        a.score_h,
        a.score_a,
        a.fg_ind,
        a.shot_result,
        a.shot_val,
        a.shot_dist,
        a.act_type,
        a.play_desc

    from playbyplay a 
    inner join active_players b on a.player_id = b.player_id
    inner join active_teams c on a.team_id = c.team_id

    order by game_id, act_id

create or replace view pg as
    select
    c.player_name,
    avg(a.pts) as pts_pg,
    avg(a.ast) as ast_pg,
    avg(a.reb) as reb_pg,
    avg(b.fg_pct) as avg_fg_pct,
    avg(b.fg3_pct) as avg_fg3_pct,
    avg(b.ft_pct) as avg_ft_pct,
    avg(b.fga) as fga_pg,
    avg(b.fg3a) as fg3a_pg,
    avg(b.fta) as fta_pg

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    
    group by c.player_name

    order by pts_pg desc;

create or replace view wins as 
    select 
        sum(a.win_ind) 
    from team_gamelog a 
    inner join active_teams b on a.team_id = b.team_id 
    where b.team = 'LAL';
    
    

create or replace view pbp_season_counts as 
    select b.season_id, count(distinct a.game_id) as games 
    
    from playbyplay a
    inner join game b on a.game_id = b.game_id
    where b.game_type = 2 
    group by b.season_id;