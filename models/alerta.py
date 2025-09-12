from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Alerta:
    produto_id: int
    quantidade_atual: int
    stock_minimo: int
    id_alerta: Optional[int] = None            # opcional, vem depois dos obrigatórios
    data_alerta: Optional[datetime] = None     # opcional, vem depois dos obrigatórios
    status: str = "ativo"                      # opcional, default "ativo"

    def esta_ativo(self) -> bool:
        """Retorna True se o alerta está ativo (stock abaixo ou igual ao mínimo)."""
        return self.status == "ativo"

    def atualizar_status(self, quantidade_atual: int):
        """Atualiza o status do alerta com base no stock atual."""
        self.quantidade_atual = quantidade_atual
        self.status = "ativo" if self.quantidade_atual <= self.stock_minimo else "resolvido"

    def __repr__(self):
        return f"<Alerta {self.id_alerta} - Produto {self.produto_id} ({self.status})>"