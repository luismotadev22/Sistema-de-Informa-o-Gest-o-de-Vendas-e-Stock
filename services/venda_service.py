from dao.venda_dao import VendaDAO
from dao.produto_dao import ProdutoDAO
from dao.alerta_dao import AlertaDAO
from models.venda import Venda

class VendaService:
    def __init__(self):
        self.venda_dao = VendaDAO()
        self.produto_dao = ProdutoDAO()
        self.alerta_dao = AlertaDAO()

    def registrar_venda(self, produto_id, quantidade, preco_unitario):
        # 1. Criar venda
        venda = Venda(
            id_venda=None,
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            total=quantidade * preco_unitario
        )
        self.venda_dao.inserir(venda)

        # 2. Atualizar stock
        produto = self.produto_dao.buscar_por_id(produto_id)
        novo_stock = produto.stock_atual - quantidade
        self.produto_dao.atualizar_stock(produto_id, novo_stock)

        # 3. Verificar se precisa de alerta
        if novo_stock <= produto.stock_minimo:
            self.alerta_dao.criar_alerta(produto_id, novo_stock, produto.stock_minimo)

    def listar_vendas(self):
        return self.venda_dao.listar()