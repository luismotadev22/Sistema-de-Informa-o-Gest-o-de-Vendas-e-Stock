from typing import List
from dao.produto_dao import ProdutoDAO
from models.produto import Produto

class ProdutoService:
    def __init__(self):
        self.produto_dao = ProdutoDAO()

    def listar_produtos(self) -> List[Produto]:
        """Retorna todos os produtos."""
        return self.produto_dao.listar_todos()

    def obter_por_id(self, id_produto: int) -> Produto | None:
        """Retorna um produto pelo ID."""
        return self.produto_dao.obter_por_id(id_produto)

    def adicionar_produto(self, produto: Produto) -> int | None:
        """Insere um novo produto e retorna o ID."""
        return self.produto_dao.inserir(produto)

    def atualizar_produto(self, produto: Produto) -> bool:
        """Atualiza um produto existente."""
        return self.produto_dao.atualizar(produto)

    def remover_produto(self, id_produto: int) -> bool:
        """Remove um produto pelo ID."""
        return self.produto_dao.remover(id_produto)
