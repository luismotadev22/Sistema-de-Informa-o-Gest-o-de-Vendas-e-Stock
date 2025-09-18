from typing import Optional, List
from db.db_connection import get_connection
from models.produto import Produto
from mysql.connector import Error
from datetime import datetime

class ProdutoDAO:
    def inserir(self, produto: Produto) -> Optional[int]:
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO produtos (nome, preco_venda, custo_aquisicao, stock_atual, stock_minimo)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (produto.nome, produto.preco_venda, produto.custo_aquisicao, produto.stock_atual, produto.stock_minimo)
            )
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"❌ Erro ao inserir produto: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def listar_todos(self) -> List[Produto]:
        produtos = []
        conn = get_connection()
        if not conn:
            return produtos
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM produtos ORDER BY id_produto ASC;")
            rows = cursor.fetchall()
            for row in rows:
                data = row.get("criado_em")
                if isinstance(data, str):
                    try:
                        data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        data = None
                produtos.append(Produto(
                    id_produto=row["id_produto"],
                    nome=row["nome"],
                    preco_venda=float(row["preco_venda"]),
                    custo_aquisicao=float(row["custo_aquisicao"]),
                    stock_atual=row["stock_atual"],
                    stock_minimo=row["stock_minimo"],
                    data_registo=data
                ))
            return produtos
        finally:
            cursor.close()
            conn.close()

    def obter_por_id(self, id_produto: int) -> Optional[Produto]:
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM produtos WHERE id_produto=%s", (id_produto,))
            row = cursor.fetchone()
            if row:
                data = row.get("criado_em")
                if isinstance(data, str):
                    try:
                        data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        data = None
                return Produto(
                    id_produto=row["id_produto"],
                    nome=row["nome"],
                    preco_venda=float(row["preco_venda"]),
                    custo_aquisicao=float(row["custo_aquisicao"]),
                    stock_atual=row["stock_atual"],
                    stock_minimo=row["stock_minimo"],
                    data_registo=data
                )
            return None
        finally:
            cursor.close()
            conn.close()

    def atualizar(self, produto: Produto) -> bool:
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE produtos
            SET nome=%s, preco_venda=%s, custo_aquisicao=%s, stock_atual=%s, stock_minimo=%s
            WHERE id_produto=%s
            """
            cursor.execute(sql, (
                produto.nome,
                produto.preco_venda,
                produto.custo_aquisicao,
                produto.stock_atual,
                produto.stock_minimo,
                produto.id_produto
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()