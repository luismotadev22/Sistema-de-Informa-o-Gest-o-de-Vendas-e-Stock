from typing import List, Optional
from db.db_connection import get_connection
from models.venda import Venda
from mysql.connector import Error
from datetime import datetime

class VendaDAO:
    def inserir(self, venda: Venda) -> Optional[int]:
        """Insere uma nova venda na tabela vendas."""
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
            cursor.execute(
                sql,
                (venda.produto_id, venda.quantidade, venda.preco_unitario, total, venda.data_venda),
            )
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
        """Lista todas as vendas registadas."""
        vendas = []
        conn = get_connection()
        if not conn:
            return vendas
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM vendas ORDER BY data_venda DESC;")
            rows = cursor.fetchall()
            for row in rows:
                vendas.append(
                    Venda(
                        id_venda=row["id_venda"],
                        produto_id=row["produto_id"],
                        quantidade=row["quantidade"],
                        preco_unitario=row["preco_unitario"],
                        total=row["total"],
                        data_venda=row["data_venda"] if row["data_venda"] else datetime.now()
                    )
                )
            return vendas
        except Error as e:
            print(f"❌ Erro ao listar vendas: {e}")
            return vendas
        finally:
            cursor.close()
            conn.close()

    def atualizar_total(self, id_venda: int, quantidade: int, preco_unitario: float) -> bool:
        """Atualiza quantidade, preço unitário e total de uma venda."""
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            total = quantidade * preco_unitario
            sql = """
            UPDATE vendas
            SET quantidade=%s, preco_unitario=%s, total=%s
            WHERE id_venda=%s
            """
            cursor.execute(sql, (quantidade, preco_unitario, total, id_venda))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Erro ao atualizar venda: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def vendas_diarias(self, start_date=None, end_date=None):
        """
        Retorna lista de dicts: [{'dia': date, 'total_vendido': Decimal, 'num_vendas': int}, ...]
        Se start_date e end_date forem fornecidos (strings 'YYYY-MM-DD'), filtra o intervalo.
        """
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

            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"❌ Erro vendas_diarias: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def produtos_mais_vendidos(self, limite: int = 10, start_date=None, end_date=None):
        """
        Retorna top produtos (id, nome, quantidade_total, valor_total).
        Pode filtrar por intervalo de datas (start_date, end_date).
        """
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

            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"❌ Erro produtos_mais_vendidos: {e}")
            return []
        finally:
            cursor.close()
            conn.close()