import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.produto_service import ProdutoService
from models.produto import Produto

class ProdutosView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.service = ProdutoService()

        # 🔹 Título
        title_frame = tb.Frame(self)
        title_frame.pack(fill="x", pady=(0, 10))
        self.lbl_title = tb.Label(
            title_frame, text="📦 Gestão de Produtos",
            font=("Segoe UI", 18, "bold"),
            bootstyle="inverse-primary"
        )
        self.lbl_title.pack(anchor="w", padx=10, pady=5)

        # 🔹 Barra de botões (toolbar)
        toolbar = tb.Frame(self)
        toolbar.pack(fill="x", pady=(0, 10))
        tb.Button(toolbar, text="➕ Adicionar", bootstyle="success", command=self.adicionar_produto).pack(side="left", padx=5)
        tb.Button(toolbar, text="🔄 Recarregar", bootstyle="info", command=self.carregar_produtos).pack(side="left", padx=5)

        # 🔹 Frame da tabela com Scrollbars
        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Nome", "Preço Venda", "Custo Aquisição", "Stock Atual", "Stock Mínimo", "Data Registo"),
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

        self.carregar_produtos()

    def carregar_produtos(self):
        """Limpa e recarrega a Treeview com os produtos."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        for produto in self.service.listar_produtos():
            data_str = produto.data_registo.strftime("%d/%m/%Y %H:%M:%S") if produto.data_registo else ""
            self.tree.insert(
                "",
                "end",
                values=(
                    produto.id_produto,
                    produto.nome,
                    f"{produto.preco_venda:.2f} €",
                    f"{produto.custo_aquisicao:.2f} €",
                    produto.stock_atual,
                    produto.stock_minimo,
                    data_str
                )
            )

    def adicionar_produto(self):
        """Popup para adicionar novo produto."""
        popup = ProdutoPopup(self)
        self.wait_window(popup)
        if popup.result:
            produto = Produto(**popup.result)
            self.service.adicionar_produto(produto)
            self.carregar_produtos()


class ProdutoPopup(tb.Toplevel):
    """Popup para adicionar produto."""
    def __init__(self, master):
        super().__init__(master)
        self.title("➕ Adicionar Produto")
        self.result = None
        self.grab_set()

        # 🔹 Frame principal com padding
        content = tb.Frame(self, padding=15)
        content.pack(fill="both", expand=True)

        # Campos do formulário
        labels = ["Nome:", "Preço Venda:", "Custo Aquisição:", "Stock Atual:", "Stock Mínimo:"]
        self.entries = {}

        for i, label in enumerate(labels):
            tb.Label(content, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tb.Entry(content, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        # Botão Confirmar
        btn = tb.Button(content, text="Confirmar", bootstyle="primary", command=self.confirmar)
        btn.grid(row=len(labels), column=0, columnspan=2, pady=15)

    def confirmar(self):
        try:
            nome = self.entries["Nome:"].get()
            preco_venda = float(self.entries["Preço Venda:"].get())
            custo_aquisicao = float(self.entries["Custo Aquisição:"].get())
            stock_atual = int(self.entries["Stock Atual:"].get())
            stock_minimo = int(self.entries["Stock Mínimo:"].get())

            if not nome:
                raise ValueError("Nome não pode estar vazio.")
            if preco_venda <= 0 or custo_aquisicao <= 0:
                raise ValueError("Preço e custo devem ser positivos.")
            if stock_atual < 0 or stock_minimo < 0:
                raise ValueError("Stock não pode ser negativo.")

        except Exception as e:
            messagebox.showerror("Erro", f"Dados inválidos: {e}")
            return

        self.result = {
            "nome": nome,
            "preco_venda": preco_venda,
            "custo_aquisicao": custo_aquisicao,
            "stock_atual": stock_atual,
            "stock_minimo": stock_minimo
        }
        self.destroy()