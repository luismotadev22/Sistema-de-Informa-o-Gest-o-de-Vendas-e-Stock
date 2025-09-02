import tkinter as tk
from tkinter import ttk
from services.relatorio_service import RelatorioService

class RelatoriosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.service = RelatorioService()

        ttk.Label(self, text="📈 Relatórios", font=("Segoe UI", 14, "bold")).pack(pady=10)

        ttk.Button(self, text="📊 Vendas por Produto", command=self.mostrar_vendas_por_produto).pack(pady=5)
        ttk.Button(self, text="⚠️ Produtos com pouco stock", command=self.mostrar_produtos_com_pouco_stock).pack(pady=5)

        self.output = tk.Text(self, height=20, width=80)
        self.output.pack(padx=10, pady=10)

    def mostrar_vendas_por_produto(self):
        dados = self.service.vendas_por_produto()
        self.output.delete("1.0", tk.END)
        for linha in dados:
            self.output.insert(tk.END, f"{linha}\n")

    def mostrar_produtos_com_pouco_stock(self):
        dados = self.service.produtos_com_pouco_stock()
        self.output.delete("1.0", tk.END)
        for linha in dados:
            self.output.insert(tk.END, f"{linha}\n")
