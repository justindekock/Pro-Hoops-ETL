import mariadb
import pandas as pd
from dba import connect_mariadb, disconnect, select_count, show_tables, show_columns

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
    #vals_ph = ('?, ' * len(fields))[:-2]
    vals_ph = ', '.join(['%s'] * len(fields))
    fields_str = ', '.join(fields)
    insert_query = f'insert ignore into {table} ({fields_str}) values {vals_ph};'
    
    pre_count = select_count(table)
    conn, cur = connect_mariadb()
    cur.execute(insert_query, values)
    post_count = select_count(table)
    new_recs = post_count - pre_count
    
    if new_recs > 0: 
        conn.commit()
        print(f'Committed insert of {new_recs} new records')
    else: 
        print(f'No new records found after insert')
        
    disconnect(conn)

insert_into('test', ['col1', 'col2', 'col3', 'col4'], (6, 'op', 2, '2025-03-11'))




def insert_game_logs(game_logs):
    # pass the fields and values lists to this, and call the insert_into function for each one
    
    pass
    


    
    