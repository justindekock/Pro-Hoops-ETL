import mariadb
import pandas as pd
from database.dba import connect_mariadb, disconnect, select_count_conn, show_tables, show_columns

def insert_into(table, fields, values):
    vals_ph = ', '.join(['%s'] * len(fields))
    fields_str = ', '.join(fields)
    insert_query = f'insert ignore into {table} ({fields_str}) values ({vals_ph});'

    conn, cur = connect_mariadb()
    pre_count = select_count_conn(cur, table) 
    post_count = pre_count # update post count in the try block
    print(insert_query)
    
    try:
        for value in values:
            cur.execute(insert_query, value)       
        
    except mariadb.Error as e:
        print(e)
        
    post_count = select_count_conn(cur, table) 
    print(f'Records in {table} after insert: {post_count}')
    new_recs = post_count - pre_count
    if new_recs > 0: 
        conn.commit()
        print(f'Committed insert of {new_recs} new records')
    else: 
        print(f'No new records found after insert')
        
    disconnect(conn)







    
    