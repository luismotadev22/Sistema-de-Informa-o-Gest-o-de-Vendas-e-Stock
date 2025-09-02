import tkinter as tk
from ui.produtos_view import ProdutosView

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Vendas e Stock")
        self.geometry("400x300")

        btn_produtos = tk.Button(self, text="Gerir Produtos", command=self.abrir_produtos)
        btn_produtos.pack(pady=20)

    def abrir_produtos(self):
        ProdutosView(self)