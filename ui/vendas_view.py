import tkinter as tk
from tkinter import ttk
from services.venda_service import VendaService

class VendasView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.service = VendaService()

        ttk.Label(self, text="🛒 Registo de Vendas", font=("Segoe UI", 14, "bold")).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Produto ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_produto = ttk.Entry(form)
        self.entry_produto.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_qtd = ttk.Entry(form)
        self.entry_qtd.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Preço Unitário:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_preco = ttk.Entry(form)
        self.entry_preco.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form, text="💾 Registrar Venda", command=self.registrar_venda).grid(row=3, column=0, columnspan=2, pady=10)

    def registrar_venda(self):
        produto_id = int(self.entry_produto.get())
        quantidade = int(self.entry_qtd.get())
        preco = float(self.entry_preco.get())
        self.service.registrar_venda(produto_id, quantidade, preco)
        tk.messagebox.showinfo("✅ Sucesso", "Venda registrada com sucesso!")