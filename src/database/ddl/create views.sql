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