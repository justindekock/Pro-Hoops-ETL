import mariadb
import pandas as pd
from dbconfig import connect_mariadb, disconnect

def select_count(table):
    query = f'select count(*) from {table}'
    conn, cur = connect_mariadb()
    cur.execute(query)
    recs = cur.fetchone()
    disconnect(conn)
    return recs[0]

#print(select_count('test'))

def select(query, fetch_type):
    conn, cur = connect_mariadb()
    cur.execute(query)    
    if fetch_type == 'all':
        result = cur.fetchall()
    elif fetch_type == 'one':
        result = cur.fetchone()
    elif fetch_type == 'df':
        result = pd.read_sql(query, conn)
    disconnect(conn)
    return result
    
#print(select('select * from test', 'all'))

# TODO - create one function where you pass a table name and list of values, then another where you call that on a list of lists of values
def insert_into(table, fields, values):
    vals_ph = ('?, ' * len(fields))[:-2]
    #print(vals_ph)
    
    fields_str = ', '.join(fields)
    print(fields_str)
    insert_query = f"""
    insert ignore into {table} ({fields_str})
    {vals_ph} 
    """
    return insert_query


print(insert_into('game', ['col1', 'col2', 'col3', 'col4', 'col5'], [6, 7, 8, 9, 10]))




def insert_game_logs(game_logs):
    # pass the fields and values lists to this, and call the insert_into function for each one
    
    pass
    


    
    