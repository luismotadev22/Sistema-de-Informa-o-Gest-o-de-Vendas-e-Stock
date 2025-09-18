from typing import List, Optional
from dao.relatorio_dao import RelatorioDAO
from models.relatorio import VendaDiaria, ProdutoMaisVendido


class RelatorioService:
    def __init__(self):
        self.dao = RelatorioDAO()

    def vendas_por_dia(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[VendaDiaria]:
        """
        Retorna lista de objetos VendaDiaria
        """
        return self.dao.vendas_diarias(start_date, end_date)

    def produtos_mais_vendidos(
        self, limite: int = 10, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[ProdutoMaisVendido]:
        """
        Retorna lista de objetos ProdutoMaisVendido
        """
        return self.dao.produtos_mais_vendidos(limite, start_date, end_date)