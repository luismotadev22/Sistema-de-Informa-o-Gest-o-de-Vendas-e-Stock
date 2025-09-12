from dao.venda_dao import VendaDAO
from collections import defaultdict
from typing import List

class RelatorioService:
    def __init__(self):
        self.dao = VendaDAO()

    def vendas_por_dia(self) -> dict:
        """Retorna dicionário: {data: total_vendas}"""
        relatorio = defaultdict(float)
        for venda in self.dao.listar():
            dia = venda.data_venda.date()  # já é datetime
            relatorio[dia] += venda.total
        return dict(relatorio)

    def produtos_mais_vendidos(self) -> List[dict]:
        """Retorna lista de produtos mais vendidos"""
        resumo = defaultdict(lambda: {"quantidade": 0, "valor_total": 0})
        for venda in self.dao.listar():
            resumo[venda.produto_id]["quantidade"] += venda.quantidade
            resumo[venda.produto_id]["valor_total"] += venda.total
        lista = [{"produto_id": k, **v} for k, v in resumo.items()]
        return sorted(lista, key=lambda x: x["quantidade"], reverse=True)