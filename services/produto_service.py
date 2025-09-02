from dao.produto_dao import ProdutoDAO
from models.produto import Produto

class ProdutoService:
    @staticmethod
    def listar_produtos():
        return ProdutoDAO.listar_todos()

    @staticmethod
    def adicionar_produto(nome, preco_venda, custo_aquisicao, stock_atual, stock_minimo):
        produto = Produto(
            nome=nome,
            preco_venda=preco_venda,
            custo_aquisicao=custo_aquisicao,
            stock_atual=stock_atual,
            stock_minimo=stock_minimo
        )
        ProdutoDAO.inserir(produto)