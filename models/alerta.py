class Alerta:
    def __init__(self, id_alerta, produto_id, quantidade_atual, stock_minimo, data_hora=None, status="ativo"):
        self.id_alerta = id_alerta
        self.produto_id = produto_id
        self.quantidade_atual = quantidade_atual
        self.stock_minimo = stock_minimo
        self.data_hora = data_hora
        self.status = status

    def __repr__(self):
        return f"<Alerta {self.id_alerta} - Produto {self.produto_id} ({self.status})>"