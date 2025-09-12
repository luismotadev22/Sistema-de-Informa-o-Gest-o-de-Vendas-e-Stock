from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Venda:
    produto_id: int
    quantidade: int
    preco_unitario: float
    total: float
    id_venda: Optional[int] = None
    data_venda: datetime = field(default_factory=datetime.now)

    def calcular_total(self) -> float:
        """Calcula o valor total da venda e atualiza o campo 'total'."""
        self.total = self.quantidade * self.preco_unitario
        return self.total