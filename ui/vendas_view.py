import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.venda_service import VendaService
from services.produto_service import ProdutoService


class VendasView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.service = VendaService()
        self.produto_service = ProdutoService()

        # 🔹 Título
        title_frame = tb.Frame(self)
        title_frame.pack(fill="x", pady=(0, 10))
        self.lbl_title = tb.Label(
            title_frame, text="🛒 Gestão de Vendas",
            font=("Segoe UI", 18, "bold"),
            bootstyle="inverse-primary"
        )
        self.lbl_title.pack(anchor="w", padx=10, pady=5)

        # 🔹 Toolbar
        toolbar = tb.Frame(self)
        toolbar.pack(fill="x", pady=(0, 10))
        tb.Button(toolbar, text="➕ Registrar Venda", bootstyle="success", command=self.adicionar_venda).pack(side="left", padx=5)
        tb.Button(toolbar, text="🔄 Recarregar", bootstyle="info", command=self.carregar_vendas).pack(side="left", padx=5)

        # 🔹 Frame da tabela com scrollbars
        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Produto ID", "Nome Produto", "Qtd", "Preço Unit.", "Total", "Data"),
            show="headings", height=15
        )

        # Cabeçalhos
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", stretch=True)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.carregar_vendas()

    def carregar_vendas(self):
        """Limpa e recarrega a Treeview com as vendas."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        for venda in self.service.listar_vendas():
            produto = self.produto_service.obter_por_id(venda.produto_id)
            nome_produto = produto.nome if produto else "❓ Desconhecido"
            self.tree.insert(
                "",
                "end",
                values=(
                    venda.id_venda,
                    venda.produto_id,
                    nome_produto,
                    venda.quantidade,
                    f"{venda.preco_unitario:.2f} €",
                    f"{venda.total:.2f} €",
                    venda.data_venda.strftime("%d/%m/%Y %H:%M:%S") if venda.data_venda else ""
                )
            )

    def adicionar_venda(self):
        """Popup para registrar uma nova venda."""
        popup = VendaPopup(self)
        self.wait_window(popup)
        if popup.result:
            produto_id, quantidade, preco_unitario = popup.result
            self.service.registar_venda(produto_id, quantidade, preco_unitario)
            self.carregar_vendas()


class VendaPopup(tb.Toplevel):
    """Popup para registrar venda."""
    def __init__(self, master):
        super().__init__(master)
        self.title("➕ Registrar Venda")
        self.result = None
        self.grab_set()

        self.produto_service = ProdutoService()

        # 🔹 Frame principal
        content = tb.Frame(self, padding=15)
        content.pack(fill="both", expand=True)

        # Produto
        tb.Label(content, text="Produto:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.produtos = self.produto_service.listar_produtos()
        self.produto_var = tb.StringVar()
        self.produto_combo = tb.Combobox(
            content,
            textvariable=self.produto_var,
            values=[f"{p.id_produto} - {p.nome}" for p in self.produtos],
            state="readonly",
            width=30
        )
        self.produto_combo.grid(row=0, column=1, padx=10, pady=5)

        # 🔹 Preencher preço automaticamente ao selecionar produto
        self.produto_combo.bind("<<ComboboxSelected>>", self.preencher_preco)
        
        # Quantidade
        tb.Label(content, text="Quantidade:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.quantidade_entry = tb.Entry(content, width=20)
        self.quantidade_entry.grid(row=1, column=1, padx=10, pady=5)

        # Preço Unitário
        tb.Label(content, text="Preço Unitário:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.preco_entry = tb.Entry(content, width=20)
        self.preco_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botão Confirmar
        btn = tb.Button(content, text="Confirmar", bootstyle="primary", command=self.confirmar)
        btn.grid(row=3, column=0, columnspan=2, pady=15)

    def preencher_preco(self, event=None):
        """Preenche o campo de preço com o preco_venda do produto escolhido."""
        produto_str = self.produto_var.get()
        if not produto_str:
            return
        try:
            produto_id = int(produto_str.split(" - ")[0])
            produto = next((p for p in self.produtos if p.id_produto == produto_id), None)
            if produto:
                self.preco_entry.delete(0, "end")
                self.preco_entry.insert(0, f"{produto.preco_venda:.2f}")
        except Exception as e:
            print("Erro ao preencher preço:", e)

    def confirmar(self):
        try:
            produto_str = self.produto_var.get()
            if not produto_str:
                raise ValueError("Selecione um produto.")
            produto_id = int(produto_str.split(" - ")[0])
            quantidade = int(self.quantidade_entry.get())
            preco_unitario = float(self.preco_entry.get())

            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            if preco_unitario <= 0:
                raise ValueError("Preço unitário deve ser maior que zero.")

        except Exception as e:
            messagebox.showerror("Erro", f"Dados inválidos: {e}")
            return

        self.result = (produto_id, quantidade, preco_unitario)
        self.destroy()
