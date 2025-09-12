import tkinter as tk
from ui.produtos_view import ProdutosView
from ui.vendas_view import VendasView
from ui.relatorios_view import RelatoriosView

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Vendas e Stock")
        self.root.geometry("1200x800")

        # Menu topo
        menubar = tk.Menu(self.root)
        produtos_menu = tk.Menu(menubar, tearoff=0)
        produtos_menu.add_command(label="Listar Produtos", command=self.show_produtos)
        menubar.add_cascade(label="Produtos", menu=produtos_menu)

        vendas_menu = tk.Menu(menubar, tearoff=0)
        vendas_menu.add_command(label="Listar Vendas", command=self.show_vendas)
        menubar.add_cascade(label="Vendas", menu=vendas_menu)

        relatorios_menu = tk.Menu(menubar, tearoff=0)
        relatorios_menu.add_command(label="Ver Relatórios", command=self.show_relatorios)
        menubar.add_cascade(label="Relatórios", menu=relatorios_menu)

        self.root.config(menu=menubar)

        # Área principal
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Views
        self.produtos_view = ProdutosView(self.container)
        self.vendas_view = VendasView(self.container)
        self.relatorios_view = RelatoriosView(self.container)

        self.show_produtos()

    def hide_all(self):
        self.produtos_view.pack_forget()
        self.vendas_view.pack_forget()
        self.relatorios_view.pack_forget()

    def show_produtos(self):
        self.hide_all()
        self.produtos_view.pack(fill="both", expand=True)

    def show_vendas(self):
        self.hide_all()
        self.vendas_view.pack(fill="both", expand=True)

    def show_relatorios(self):
        self.hide_all()
        self.relatorios_view.pack(fill="both", expand=True)
