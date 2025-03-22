import mariadb
from database.dba import connect_mariadb, disconnect, select_count_conn
from log_config.logs import get_logger
from gmail.gmail import gmail_log_write

logger = get_logger(__name__)

def insert_into(gmail_log, table, fields, values, database=None):
    vals_ph = ', '.join(['%s'] * len(fields))
    fields_str = ', '.join(fields)
    insert_query = f'insert ignore into {table} ({fields_str}) values ({vals_ph});'
    logger.debug(f'Insert statement generated: {insert_query}')

    if not database:
        conn, cur = connect_mariadb()
    else:
        conn, cur = connect_mariadb(database)    
    
    pre_count = select_count_conn(cur, table) 
    post_count = pre_count # update post count in the try block
    logger.debug(f'Records in {table} before insert: {pre_count}')
    
    try:
        for value in values:
            cur.execute(insert_query, value)
                
        post_count = select_count_conn(cur, table) 
        new_recs = post_count - pre_count
        
        gmail_log_write(gmail_log, f"""-- {new_recs} new records inserted in {table}
---- {post_count} records now exist in {table}
""")
        
        # logger.debug(f'Inserts executed successfully!')
        if new_recs > 0: 
            conn.commit()
            logger.info(f'Committed insert of {new_recs} new records into {table} -- {post_count} records now exist in table')
            
        else: 
            logger.info(f'Insert function executed successfully, but no new records were inserted into {table}')
        
    except mariadb.Error:
        logger.exception('Could not insert records:')
        raise
    
    disconnect(conn)
    
# function to convert df to a list of fields and list of values, used to pass to insert_into
def df_to_insert_lists(df):
    fields = []
    vals = []
    
    fields_np = df.columns
    for field in fields_np:
        fields.append(field)
    
    vals_np = df.to_numpy()
    for val in vals_np:
        val = list(val)
        vals.append(val)
        
    return [fields, vals]

# converts list of clean game log dfs to lists that insert_into will accept
def separate_dfs(dfs_list):
    insert_lists = []
    for df in dfs_list:
        insert_lists.append(df_to_insert_lists(df))
    return insert_lists

# for loop to execute the inserts on all tables
def insert_into_tables(gmail_log, tables, fields_vals_lists, database=None):
    for i, table in enumerate(tables):
        
        if not database:
            insert_into(gmail_log, table=table, 
                fields=fields_vals_lists[i][0],
                values=fields_vals_lists[i][1])
        else:
            insert_into(gmail_log, table=table, 
                fields=fields_vals_lists[i][0],
                values=fields_vals_lists[i][1],
                database=database)
            
        
def insert_pbp(gmail_log, table, fields_vals_list, database=None):
    for fields_vals in fields_vals_list:
        if not database:
            insert_into(gmail_log, table = table,
                    fields=fields_vals[0],
                    values=fields_vals[1])
        else:
            insert_into(gmail_log, table = table,
                    fields=fields_vals[0],
                    values=fields_vals[1],
                    database=database)




    
    