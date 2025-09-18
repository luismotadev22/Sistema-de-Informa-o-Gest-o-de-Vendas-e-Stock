from dao.venda_dao import VendaDAO
from dao.produto_dao import ProdutoDAO
from dao.alerta_dao import AlertaDAO
from models.venda import Venda
from models.alerta import Alerta

class VendaService:
    def __init__(self):
        self.venda_dao = VendaDAO()
        self.produto_dao = ProdutoDAO()
        self.alerta_dao = AlertaDAO()

    def registar_venda(self, produto_id: int, quantidade: int, preco_unitario: float) -> bool:
        produto = self.produto_dao.obter_por_id(produto_id)
        if not produto:
            print(f"❌ Produto {produto_id} não encontrado.")
            return False

        if produto.stock_atual < quantidade:
            print(f"❌ Stock insuficiente para o produto '{produto.nome}'.")
            return False

        venda = Venda(
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            total=quantidade * preco_unitario
        )
        venda_id = self.venda_dao.inserir(venda)
        if not venda_id:
            return False

        produto.stock_atual -= quantidade
        self.produto_dao.atualizar(produto)

        if produto.stock_atual <= produto.stock_minimo:
            alerta = Alerta(
                id_alerta=None,
                produto_id=produto_id,
                quantidade_atual=produto.stock_atual,
                stock_minimo=produto.stock_minimo,
                status="ativo",
                data_alerta=None
            )
            self.alerta_dao.inserir(alerta)

        return True

    def listar_vendas(self):
        return self.venda_dao.listar()

    def vendas_diarias(self, start_date=None, end_date=None):
        return self.venda_dao.vendas_diarias(start_date, end_date)

    def produtos_mais_vendidos(self, limite=10, start_date=None, end_date=None):
        return self.venda_dao.produtos_mais_vendidos(limite, start_date, end_date)