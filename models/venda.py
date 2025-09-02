class Venda:
    def __init__(self, id_venda, produto_id, quantidade, preco_unitario, total=None, data_hora=None, status="confirmada"):
        self.id_venda = id_venda
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.total = total if total is not None else quantidade * preco_unitario
        self.data_hora = data_hora
        self.status = status

    def __repr__(self):
        return f"<Venda {self.id_venda} - Produto {self.produto_id} ({self.quantidade} un.)>"