from typing import List, Optional
from db.db_connection import get_connection
from models.venda import Venda
from mysql.connector import Error
from datetime import datetime

class VendaDAO:
    def inserir(self, venda: Venda) -> Optional[int]:
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        try:
            total = venda.quantidade * venda.preco_unitario
            sql = """
            INSERT INTO vendas (produto_id, quantidade, preco_unitario, total, data_venda)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                venda.produto_id,
                venda.quantidade,
                venda.preco_unitario,
                total,
                venda.data_venda
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"❌ Erro ao inserir venda: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def listar(self) -> List[Venda]:
        vendas = []
        conn = get_connection()
        if not conn:
            return vendas
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM vendas ORDER BY data_venda DESC;")
            rows = cursor.fetchall()
            for row in rows:
                vendas.append(Venda(
                    id_venda=row["id_venda"],
                    produto_id=row["produto_id"],
                    quantidade=row["quantidade"],
                    preco_unitario=row["preco_unitario"],
                    total=row["total"],
                    data_venda=row["data_venda"] if row["data_venda"] else datetime.now()
                ))
            return vendas
        except Error as e:
            print(f"❌ Erro ao listar vendas: {e}")
            return vendas
        finally:
            cursor.close()
            conn.close()

    def vendas_diarias(self, start_date=None, end_date=None):
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            if start_date and end_date:
                sql = """
                SELECT DATE(data_venda) AS dia,
                       SUM(total) AS total_vendido,
                       COUNT(*) AS num_vendas
                FROM vendas
                WHERE DATE(data_venda) BETWEEN %s AND %s
                GROUP BY dia
                ORDER BY dia ASC
                """
                cursor.execute(sql, (start_date, end_date))
            else:
                sql = """
                SELECT DATE(data_venda) AS dia,
                       SUM(total) AS total_vendido,
                       COUNT(*) AS num_vendas
                FROM vendas
                GROUP BY dia
                ORDER BY dia ASC
                """
                cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def produtos_mais_vendidos(self, limite: int = 10, start_date=None, end_date=None):
        conn = get_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        try:
            if start_date and end_date:
                sql = """
                SELECT p.id_produto, p.nome,
                       SUM(v.quantidade) AS quantidade_total,
                       SUM(v.total) AS valor_total
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id_produto
                WHERE DATE(v.data_venda) BETWEEN %s AND %s
                GROUP BY p.id_produto, p.nome
                ORDER BY quantidade_total DESC
                LIMIT %s
                """
                cursor.execute(sql, (start_date, end_date, limite))
            else:
                sql = """
                SELECT p.id_produto, p.nome,
                       SUM(v.quantidade) AS quantidade_total,
                       SUM(v.total) AS valor_total
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id_produto
                GROUP BY p.id_produto, p.nome
                ORDER BY quantidade_total DESC
                LIMIT %s
                """
                cursor.execute(sql, (limite,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()