from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class VendaDiaria:
    dia: date
    total_vendido: float
    num_vendas: int