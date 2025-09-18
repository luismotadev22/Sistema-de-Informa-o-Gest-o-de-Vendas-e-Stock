from dataclasses import dataclass
from datetime import date

@dataclass
class ProdutoMaisVendido:
    produto_id: int
    nome: str
    quantidade_total: int = 0
    valor_total: float = 0.0
    
@dataclass
class VendaDiaria:
    dia: date
    total_vendido: float
    num_vendas: int