from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Produto:
    nome: str
    preco_venda: float
    custo_aquisicao: float
    stock_atual: int
    stock_minimo: int
    data_registo: Optional[datetime] = None
    id_produto: Optional[int] = None       # opcional, vem depois dos obrigatórios
    criado_em: Optional[datetime] = None   # opcional, vem depois dos obrigatórios

    def em_alerta(self) -> bool:
        """Retorna True se o produto estiver com stock abaixo ou igual ao mínimo."""
        return self.stock_atual <= self.stock_minimo

    def margem_lucro(self) -> float:
        """Calcula a margem de lucro percentual do produto."""
        if self.custo_aquisicao == 0:
            return 0.0
        return ((self.preco_venda - self.custo_aquisicao) / self.custo_aquisicao) * 100