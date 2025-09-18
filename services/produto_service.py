from typing import List, Optional
from dao.produto_dao import ProdutoDAO
from models.produto import Produto
from models.alerta import Alerta

class ProdutoService:
    def __init__(self):
        self.produto_dao = ProdutoDAO()
        self._alerta_service = None  # Inicialização lazy

    def _get_alerta_service(self):
        """Getter lazy para evitar importação circular"""
        if self._alerta_service is None:
            from services.alerta_service import AlertaService
            self._alerta_service = AlertaService()
        return self._alerta_service

    def listar_produtos(self) -> List[Produto]:
        """Retorna todos os produtos e gera alertas se necessário."""
        produtos = self.produto_dao.listar_todos()
        alerta_service = self._get_alerta_service()

        for p in produtos:
            if p.stock_atual <= p.stock_minimo:
                # Verifica se já existe alerta ativo para este produto
                if not alerta_service.tem_alerta_ativo_para_produto(p.id_produto):
                    alerta = Alerta(
                        produto_id=p.id_produto,
                        quantidade_atual=p.stock_atual,
                        stock_minimo=p.stock_minimo,
                        status="ativo"
                    )
                    alerta_service.criar_alerta(alerta)
        return produtos

    def obter_por_id(self, id_produto: int) -> Optional[Produto]:
        return self.produto_dao.obter_por_id(id_produto)

    def adicionar_produto(self, produto: Produto) -> Optional[int]:
        produto_id = self.produto_dao.inserir(produto)
        if produto_id and produto.stock_atual <= produto.stock_minimo:
            alerta_service = self._get_alerta_service()
            alerta = Alerta(
                produto_id=produto_id,
                quantidade_atual=produto.stock_atual,
                stock_minimo=produto.stock_minimo,
                status="ativo"
            )
            alerta_service.criar_alerta(alerta)
        return produto_id

    def atualizar_produto(self, produto: Produto) -> bool:
        ok = self.produto_dao.atualizar(produto)
        if ok and produto.stock_atual <= produto.stock_minimo:
            alerta_service = self._get_alerta_service()
            if not alerta_service.tem_alerta_ativo_para_produto(produto.id_produto):
                alerta = Alerta(
                    produto_id=produto.id_produto,
                    quantidade_atual=produto.stock_atual,
                    stock_minimo=produto.stock_minimo,
                    status="ativo"
                )
                alerta_service.criar_alerta(alerta)
        return ok

    def remover_produto(self, id_produto: int) -> bool:
        return self.produto_dao.remover(id_produto)