import mariadb
from database.dbconfig import DBConfig

config = DBConfig()

def connect_mariadb():
    conn = None
    cur = None
    try: 
        conn = mariadb.connect(
            user=config.DB_USER, 
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_DATABASE
        )
        #print('Connected to mariadb server')
        cur = conn.cursor()
        
    except mariadb.Error as e: 
        print(f'Error connecting {e}')
    
    return conn, cur

def disconnect(conn):
    conn.close()
    #print('Connnection closed')
    
def select_count(table):
    query = f'select count(*) from {table}'
    conn, cur = connect_mariadb()
    cur.execute(query)
    recs = cur.fetchone()
    disconnect(conn)
    return recs[0]

def select_count_conn(cur, table):
    query = f'select count(*) from {table}'
    cur.execute(query)
    recs = cur.fetchone()
    return recs[0]
    
# conn, cur = connect_mariadb()
# disconnect(conn)

def show_tables(database):
    tables = []
    recs = []
    conn, cur = connect_mariadb()
    query = f'show tables from {database};'
    
    cur.execute(query)
    tables = cur.fetchall()
    
    for i, table in enumerate(tables): 
        recs.append(select_count(tables[i][0]))
        tables[i] = table[0]
        
    disconnect(conn)
    
    table_counts = list(zip(tables, recs))
    print(f'RECORDS IN DATABASE ({database}) TABLES:\n{table_counts}')
    
def show_columns(table):
    conn, cur = connect_mariadb()
    query = f'show columns from {table};'
    cur.execute(query)
    vals = cur.fetchall()
    cols = list(cur.description)
    disconnect(conn)
    
    for i, col in enumerate(cols):
        cols[i] = col[0]
    
    #print(cols)
    print(vals)
    
    
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
#show_tables('prohoops')
#show_columns('game')



    