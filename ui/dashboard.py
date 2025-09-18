import ttkbootstrap as tb
from tkinter import ttk
from ui.produtos_view import ProdutosView
from ui.vendas_view import VendasView
from ui.relatorios_view import RelatoriosView


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#ecf0f1")

        # Estilo ttk moderno
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#ecf0f1", borderwidth=0)
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 12, "bold"),
                        padding=[15, 8],
                        background="#bdc3c7")
        style.map("TNotebook.Tab",
                  background=[("selected", "#3498db")],
                  foreground=[("selected", "white")])

        # Notebook (abas principais)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar frames para cada view
        self.produtos_frame = ttk.Frame(self.notebook, padding=10)
        self.vendas_frame = ttk.Frame(self.notebook, padding=10)
        self.relatorios_frame = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.produtos_frame, text="📦 Produtos")
        self.notebook.add(self.vendas_frame, text="🛒 Vendas")
        self.notebook.add(self.relatorios_frame, text="📑 Relatórios")

        # Adicionar views dentro dos frames
        self.produtos_view = ProdutosView(self.produtos_frame)
        self.vendas_view = VendasView(self.vendas_frame)
        self.relatorios_view = RelatoriosView(self.relatorios_frame)

        self.produtos_view.pack(fill="both", expand=True)
        self.vendas_view.pack(fill="both", expand=True)
        self.relatorios_view.pack(fill="both", expand=True)

    def iniciar(self, aba_inicial="Produtos"):
        """Seleciona a aba inicial ao abrir o Dashboard"""
        tabs = {"Produtos": 0, "Vendas": 1, "Relatórios": 2}
        index = tabs.get(aba_inicial, 0)
        self.notebook.select(index)
        self.root.deiconify()