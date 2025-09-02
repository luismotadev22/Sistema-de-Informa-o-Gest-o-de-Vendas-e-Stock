from db.db_connection import criar_conexao

class AlertaDAO:
    @staticmethod
    def listar_todos():
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alertas;")
        alertas = cursor.fetchall()
        cursor.close()
        conn.close()
        return alertas

    @staticmethod
    def listar_ativos():
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alertas WHERE status = 'ativo';")
        ativos = cursor.fetchall()
        cursor.close()
        conn.close()
        return ativos

    @staticmethod
    def inserir(produto_id, quantidade_atual, stock_minimo, status="ativo"):
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO alertas (produto_id, quantidade_atual, stock_minimo, status)
            VALUES (%s, %s, %s, %s);
            """,
            (produto_id, quantidade_atual, stock_minimo, status)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def atualizar_status(alerta_id, status):
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alertas SET status=%s WHERE id_alerta=%s;",
            (status, alerta_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
