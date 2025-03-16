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