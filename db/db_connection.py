import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Estabelece e retorna uma conexão com a base de dados MySQL
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="grandeprogramador",
            database="gestao_vendas_stock"
        )
        if conn.is_connected():
            print("✅ Conectado à base de dados MySQL")
            return conn
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """
    Executa uma query na base de dados
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            return None
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.rowcount
            
    except Error as e:
        print(f"❌ Erro ao executar query: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()