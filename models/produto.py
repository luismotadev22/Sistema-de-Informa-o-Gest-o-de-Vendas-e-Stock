class Produto:
    def __init__(self, id_produto=None, nome="", preco_venda=0, custo_aquisicao=0, stock_atual=0, stock_minimo=0, data_registo=None):
        self.id_produto = id_produto
        self.nome = nome
        self.preco_venda = preco_venda
        self.custo_aquisicao = custo_aquisicao
        self.stock_atual = stock_atual
        self.stock_minimo = stock_minimo
        self.data_registo = data_registo