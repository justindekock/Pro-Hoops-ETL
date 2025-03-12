import mariadb

class DBConfig:
    def __init__(self):
        self.DB_USER = 'root'
        self.DB_USER = 'root'
        self.DB_PASSWORD = 'mariapw'
        self.DB_HOST = 'pi-jdeto'
        self.DB_PORT = 3306
        self.DB_DATABASE = 'prohoops'
        

        


# def connect_mariadb():
#     conn = None
#     cur = None
#     try: 
#         conn = mariadb.connect(
#             user='root', 
#             password='mariapw',
#             host='pi-jdeto',
#             port=3306,
#             database='prohoops'
#         )
#         cur = conn.cursor()
        
#     except: 
#         print('Error connecting')
    
#     return conn, cur

# def disconnect(conn):
#     conn.close()
#     print('Connnection closed')
    
    


# insert_query = """
#     insert into test (col1, col2, col3, col4) values 
#     (3, "sd", 4, "2024-03-10"),
#     (7, "pr", 5, "2025-12-05")
#     ;
# """
# select_query = 'select count(*) from test;'
# select_query2 = 'select * from test;'


# cur.execute(select_query)
# print(cur.fetchone())
# cur.execute(insert_query)
# cur.execute(select_query)
# print(cur.fetchone())

# cur.execute(select_query2)
# print(cur.fetchall())


# conn.close()