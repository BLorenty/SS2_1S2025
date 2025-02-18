import pyodbc

# COMPROBAR LA CONEXION CON LA BASE DE DATOS (ESTO ES OPCIONAL) (SQL SERVER)
server = 'ZEPHROG14\\SQLEXPRESS' # PUEDE SER LOCALHOST O LA IP DE LA MÁQUINA DONDE ESTÁ LA BASE DE DATOS
database = 'SS2_practica1' # NOMBRE DE LA BASE DE DATOS QUE SE UTILIZARÁ (CREADA ANTES)
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'


conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

def close_connection():
    conn.close()