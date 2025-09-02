from db.db_connection import criar_conexao

class VendaDAO:
    @staticmethod
    def listar_todas():
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vendas;")
        vendas = cursor.fetchall()
        cursor.close()
        conn.close()
        return vendas

    @staticmethod
    def buscar_por_id(venda_id):
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vendas WHERE id_venda = %s;", (venda_id,))
        venda = cursor.fetchone()
        cursor.close()
        conn.close()
        return venda

    @staticmethod
    def inserir(produto_id, quantidade, preco_unitario):
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO vendas (produto_id, quantidade, preco_unitario)
            VALUES (%s, %s, %s);
            """,
            (produto_id, quantidade, preco_unitario)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def atualizar_status(venda_id, status):
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vendas SET status=%s WHERE id_venda=%s;",
            (status, venda_id)
        )
        conn.commit()
        cursor.close()
        conn.close()