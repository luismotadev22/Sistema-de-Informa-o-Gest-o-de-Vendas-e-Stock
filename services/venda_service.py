from dao.produto_dao import ProdutoDAO
from dao.venda_dao import VendaDAO
from dao.alerta_dao import AlertaDAO
from models.venda import Venda
from models.alerta import Alerta


class VendaService:
    def __init__(self):
        self.venda_dao = VendaDAO()
        self.produto_dao = ProdutoDAO()
        self.alerta_dao = AlertaDAO()

    def registar_venda(self, produto_id: int, quantidade: int, preco_unitario: float) -> bool:
        """
        Regista uma venda, atualiza o stock e cria alerta se necessário.
        """
        # Buscar produto
        produto = self.produto_dao.obter_por_id(produto_id)
        if not produto:
            print(f"❌ Produto {produto_id} não encontrado.")
            return False

        # Verificar stock disponível
        if produto.stock_atual < quantidade:
            print(f"❌ Stock insuficiente para o produto '{produto.nome}'.")
            return False

        # Criar a venda
        venda = Venda(
            id_venda=None,
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            total=quantidade * preco_unitario
            
        )
        venda_id = self.venda_dao.inserir(venda)
        if not venda_id:
            print("❌ Erro ao registar a venda.")
            return False

        # Atualizar stock do produto
        produto.stock_atual -= quantidade
        if not self.produto_dao.atualizar(produto):
            print("❌ Erro ao atualizar o stock do produto.")
            return False

        # Criar alerta se stock <= stock mínimo
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

        print(f"✅ Venda registada e stock atualizado. Novo stock: {produto.stock_atual}")
        return True

    def listar_vendas(self):
        """Retorna todas as vendas registadas."""
        return self.venda_dao.listar()

    def vendas_diarias(self, start_date=None, end_date=None):
        """
        Retorna lista de dicts:
        [{'dia': date, 'total_vendido': Decimal, 'num_vendas': int}, ...]
        """
        return self.venda_dao.vendas_diarias(start_date, end_date)

    def produtos_mais_vendidos(self, limite: int = 10, start_date=None, end_date=None):
        """
        Retorna top produtos mais vendidos.
        Cada item: {'id_produto', 'nome', 'quantidade_total', 'valor_total'}
        """
        return self.venda_dao.produtos_mais_vendidos(limite, start_date, end_date)
