-- per game regular season stats
create or replace view v_pg_rs as
    select
    c.player_name,
    avg(a.pts) as pts_pg,
    avg(a.ast) as ast_pg,
    avg(a.reb) as reb_pg,
    avg(a.oreb) as oreb_pg,
    avg(a.stl) as stl_pg,
    avg(a.blk) as blk_pg,
    avg(b.fg_pct) as avg_fg_pct,
    avg(b.fgm) as fgm_pg,
    avg(b.fga) as fga_pg,
    avg(b.fg3_pct) as avg_fg3_pct,
    avg(b.fg3m) as fg3m_pg,
    avg(b.fg3a) as fg3a_pg,
    avg(b.ft_pct) as avg_ft_pct,
    avg(b.ftm) as ftm_pg,
    avg(b.fta) as fta_pg,
    avg(a.tov) as tov_pg,
    avg(a.pf) as pg_pg

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type = 2

    group by c.player_name

    order by pts_pg desc;

create or replace view v_pg_po as
    select
    c.player_name,
    avg(a.pts) as pts_pg,
    avg(a.ast) as ast_pg,
    avg(a.reb) as reb_pg,
    avg(a.oreb) as oreb_pg,
    avg(a.stl) as stl_pg,
    avg(a.blk) as blk_pg,
    avg(b.fg_pct) as avg_fg_pct,
    avg(b.fgm) as fgm_pg,
    avg(b.fga) as fga_pg,
    avg(b.fg3_pct) as avg_fg3_pct,
    avg(b.fg3m) as fg3m_pg,
    avg(b.fg3a) as fg3a_pg,
    avg(b.ft_pct) as avg_ft_pct,
    avg(b.ftm) as ftm_pg,
    avg(b.fta) as fta_pg,
    avg(a.tov) as tov_pg,
    avg(a.pf) as pg_pg

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type = 4

    group by c.player_name

    order by pts_pg desc;

create or replace view v_pg_ps as
    select
    c.player_name,
    avg(a.pts) as pts_pg,
    avg(a.ast) as ast_pg,
    avg(a.reb) as reb_pg,
    avg(a.oreb) as oreb_pg,
    avg(a.stl) as stl_pg,
    avg(a.blk) as blk_pg,
    avg(b.fg_pct) as avg_fg_pct,
    avg(b.fgm) as fgm_pg,
    avg(b.fga) as fga_pg,
    avg(b.fg3_pct) as avg_fg3_pct,
    avg(b.fg3m) as fg3m_pg,
    avg(b.fg3a) as fg3a_pg,
    avg(b.ft_pct) as avg_ft_pct,
    avg(b.ftm) as ftm_pg,
    avg(b.fta) as fta_pg,
    avg(a.tov) as tov_pg,
    avg(a.pf) as pg_pg

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type in (4, 5)

    group by c.player_name

    order by pts_pg desc;

create or replace view v_pg_fs as
    select
    c.player_name,
    avg(a.pts) as pts_pg,
    avg(a.ast) as ast_pg,
    avg(a.reb) as reb_pg,
    avg(a.oreb) as oreb_pg,
    avg(a.stl) as stl_pg,
    avg(a.blk) as blk_pg,
    avg(b.fg_pct) as avg_fg_pct,
    avg(b.fgm) as fgm_pg,
    avg(b.fga) as fga_pg,
    avg(b.fg3_pct) as avg_fg3_pct,
    avg(b.fg3m) as fg3m_pg,
    avg(b.fg3a) as fg3a_pg,
    avg(b.ft_pct) as avg_ft_pct,
    avg(b.ftm) as ftm_pg,
    avg(b.fta) as fta_pg,
    avg(a.tov) as tov_pg,
    avg(a.pf) as pg_pg

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type in (2, 4, 5)

    group by c.player_name

    order by pts_pg desc;