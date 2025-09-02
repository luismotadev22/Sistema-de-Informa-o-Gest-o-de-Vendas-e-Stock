from db.db_connection import criar_conexao
from models.produto import Produto

class ProdutoDAO:

    @staticmethod
    def listar_todos():
        conn = criar_conexao()
        produtos = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM produtos")
            for row in cursor.fetchall():
                produtos.append(Produto(**row))
            cursor.close()
            conn.close()
        return produtos

    @staticmethod
    def inserir(produto: Produto):
        conn = criar_conexao()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO produtos (nome, preco_venda, custo_aquisicao, stock_atual, stock_minimo) VALUES (%s, %s, %s, %s, %s)",
                (produto.nome, produto.preco_venda, produto.custo_aquisicao, produto.stock_atual, produto.stock_minimo)
            )
            conn.commit()
            cursor.close()
            conn.close()