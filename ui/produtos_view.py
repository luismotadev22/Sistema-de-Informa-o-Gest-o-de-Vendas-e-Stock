import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.produto_service import ProdutoService
from services.alerta_service import AlertaService
from models.produto import Produto
from models.alerta import Alerta
from datetime import datetime

# -------------------- ProdutosView --------------------
class ProdutosView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.service = ProdutoService()

        # 🔹 Título
        title_frame = tb.Frame(self)
        title_frame.pack(fill="x", pady=(0, 10))
        tb.Label(title_frame, text="📦 Gestão de Produtos",
                 font=("Segoe UI", 18, "bold"),
                 bootstyle="inverse-primary").pack(anchor="w", padx=10, pady=5)

        # 🔹 Barra de botões
        toolbar = tb.Frame(self)
        toolbar.pack(fill="x", pady=(0, 10))
        tb.Button(toolbar, text="➕ Adicionar", bootstyle="success",
                  command=self.adicionar_produto).pack(side="left", padx=5)
        tb.Button(toolbar, text="🔄 Recarregar", bootstyle="info",
                  command=self.carregar_produtos).pack(side="left", padx=5)

        # 🔹 Tabela
        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame,
                                 columns=("ID", "Nome", "Preço Venda", "Custo Aquisição", "Stock Atual", "Stock Mínimo", "Data Registo"),
                                 show="headings", height=15)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", stretch=True)

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
        for i in self.tree.get_children():
            self.tree.delete(i)

        produtos = self.service.listar_produtos()
        for p in produtos:
            data_str = p.data_registo.strftime("%d/%m/%Y %H:%M:%S") if p.data_registo else ""
            self.tree.insert("", "end", values=(
                p.id_produto, p.nome, f"{p.preco_venda:.2f} €",
                f"{p.custo_aquisicao:.2f} €",
                p.stock_atual, p.stock_minimo, data_str
            ))

    def adicionar_produto(self):
        popup = ProdutoPopup(self)
        self.wait_window(popup)
        if popup.result:
            produto = Produto(**popup.result)
            self.service.adicionar_produto(produto)
            self.carregar_produtos()

class ProdutoPopup(tb.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("➕ Adicionar Produto")
        self.result = None
        self.grab_set()
        content = tb.Frame(self, padding=15)
        content.pack(fill="both", expand=True)

        labels = ["Nome:", "Preço Venda:", "Custo Aquisição:", "Stock Atual:", "Stock Mínimo:"]
        self.entries = {}
        for i, label in enumerate(labels):
            tb.Label(content, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tb.Entry(content, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        tb.Button(content, text="Confirmar", bootstyle="primary", command=self.confirmar).grid(
            row=len(labels), column=0, columnspan=2, pady=15
        )

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
            "nome": nome, "preco_venda": preco_venda, "custo_aquisicao": custo_aquisicao,
            "stock_atual": stock_atual, "stock_minimo": stock_minimo
        }
        self.destroy()


# -------------------- AlertasView --------------------
class AlertaView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.service = AlertaService()

        # Título
        tb.Label(self, text="📢 Alertas de Stock", font=("Segoe UI", 16, "bold"),
                 bootstyle="inverse-danger").pack(anchor="w", pady=(0, 10))

        toolbar = tb.Frame(self)
        toolbar.pack(fill="x", pady=(0,10))
        tb.Button(toolbar, text="🔄 Recarregar", bootstyle="info", command=self.carregar_alertas).pack(side="left", padx=5)
        tb.Button(toolbar, text="✅ Marcar Resolvido", bootstyle="success", command=self.resolver_alerta).pack(side="left", padx=5)

        # Tabela
        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame,
                                 columns=("ID", "Produto", "Stock Atual", "Stock Mínimo", "Status", "Data"),
                                 show="headings", height=15)
        headings = [("ID",70), ("Produto",320), ("Stock Atual",100), ("Stock Mínimo",100), ("Status",100), ("Data",170)]
        for col, width in headings:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=width, stretch=False)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.tag_configure("ativo", background="#ffdd57")  # amarelo
        self.tree.tag_configure("resolvido", background="#d4edda")  # verde

        self.carregar_alertas()

    def carregar_alertas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        alertas = self.service.listar_alertas()
        for a in alertas:
            self.tree.insert("", "end",
                             values=(a.id_alerta, a.produto_id, a.quantidade_atual, a.stock_minimo, a.status, a.data_alerta),
                             tags=(a.status,))

    def resolver_alerta(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um alerta para marcar como resolvido.")
            return
        item = self.tree.item(sel[0])
        id_alerta = item["values"][0]
        if self.service.resolver_alerta(id_alerta):
            messagebox.showinfo("Sucesso", "Alerta resolvido.")
            self.carregar_alertas()
        else:
            messagebox.showerror("Erro", "Não foi possível resolver o alerta.")