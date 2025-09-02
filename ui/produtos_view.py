import tkinter as tk
from tkinter import ttk
from services.produto_service import ProdutoService

class ProdutosView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestão de Produtos")
        self.geometry("600x400")

        self.tree = ttk.Treeview(self, columns=("id", "nome", "preco", "stock"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("stock", text="Stock Atual")
        self.tree.pack(fill="both", expand=True)

        self.carregar_produtos()

    def carregar_produtos(self):
        for p in ProdutoService.listar_produtos():
            self.tree.insert("", "end", values=(p.id_produto, p.nome, p.preco_venda, p.stock_atual))