from dataclasses import dataclass
from typing import Optional

@dataclass
class ProdutoMaisVendido:
    produto_id: int
    nome: str
    quantidade_total: int = 0
    valor_total: float = 0.0