from dao.venda_dao import VendaDAO
from dao.produto_dao import ProdutoDAO

class RelatorioService:
    def __init__(self):
        self.venda_dao = VendaDAO()
        self.produto_dao = ProdutoDAO()

    def vendas_por_produto(self):
        return self.venda_dao.vendas_por_produto()

    def produtos_com_pouco_stock(self):
        return self.produto_dao.listar_com_pouco_stock()