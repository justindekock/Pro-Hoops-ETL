-- per game regular season stats
create or replace view v_totals_rs as
    select
    c.player_name,
    sum(a.pts) as pts,
    sum(a.ast) as ast,
    sum(a.reb) as reb,
    sum(a.oreb) as oreb,
    sum(a.stl) as stl,
    sum(a.blk) as blk,
    sum(b.fgm) as fgm,
    sum(b.fga) as fga,
    sum(b.fg3m) as fg3m,
    sum(b.fg3a) as fg3a,
    sum(b.ftm) as ftm,
    sum(b.fta) as fta,
    sum(a.tov) as tov,
    sum(a.pf) as pf

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    left join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type = 2

    group by a.player_id, c.player_name

    order by pts desc;

create or replace view v_totals_po as
    select
    c.player_name,
    sum(a.pts) as pts,
    sum(a.ast) as ast,
    sum(a.reb) as reb,
    sum(a.oreb) as oreb,
    sum(a.stl) as stl,
    sum(a.blk) as blk,
    sum(b.fgm) as fgm,
    sum(b.fga) as fga,
    sum(b.fg3m) as fg3m,
    sum(b.fg3a) as fg3a,
    sum(b.ftm) as ftm,
    sum(b.fta) as fta,
    sum(a.tov) as tov,
    sum(a.pf) as pf

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type = 4

    group by c.player_name

    order by pts desc;

create or replace view v_totals_ps as
    select
    c.player_name,
    sum(a.pts) as pts,
    sum(a.ast) as ast,
    sum(a.reb) as reb,
    sum(a.oreb) as oreb,
    sum(a.stl) as stl,
    sum(a.blk) as blk,
    sum(b.fgm) as fgm,
    sum(b.fga) as fga,
    sum(b.fg3m) as fg3m,
    sum(b.fg3a) as fg3a,
    sum(b.ftm) as ftm,
    sum(b.fta) as fta,
    sum(a.tov) as tov,
    sum(a.pf) as pf

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type in (4, 5)

    group by c.player_name

    order by pts desc;

create or replace view v_totals_fs as
    select
    c.player_name,
    sum(a.pts) as pts,
    sum(a.ast) as ast,
    sum(a.reb) as reb,
    sum(a.oreb) as oreb,
    sum(a.stl) as stl,
    sum(a.blk) as blk,
    sum(b.fgm) as fgm,
    sum(b.fga) as fga,
    sum(b.fg3m) as fg3m,
    sum(b.fg3a) as fg3a,
    sum(b.ftm) as ftm,
    sum(b.fta) as fta,
    sum(a.tov) as tov,
    sum(a.pf) as pf

    from player_box a 
    inner join player_shooting b on a.game_id = b.game_id 
        and a.player_id = b.player_id
    inner join active_players c on a.player_id = c.player_id
    inner join game d on a.game_id = d.game_id

    where d.game_type in (2, 4, 5)

    group by c.player_name

    order by pts desc;