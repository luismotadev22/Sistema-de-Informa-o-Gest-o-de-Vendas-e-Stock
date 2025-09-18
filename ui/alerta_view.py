import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.alerta_service import AlertaService
from services.produto_service import ProdutoService
from datetime import datetime

def format_date_safe(d):
    if not d:
        return ""
    if isinstance(d, datetime):
        return d.strftime("%d/%m/%Y %H:%M:%S")
    # pode ser string vindo do DB
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(str(d), fmt).strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            continue
    return str(d)

class AlertaView(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.service = AlertaService()
        self.produto_service = ProdutoService()

        # Título e toolbar
        title_frame = tb.Frame(self)
        title_frame.pack(fill="x", pady=(0,10))
        lbl = tb.Label(title_frame, text="📢 Alertas de Stock", font=("Segoe UI", 16, "bold"), bootstyle="inverse-danger")
        lbl.pack(anchor="w", padx=10)

        toolbar = tb.Frame(self)
        toolbar.pack(fill="x", pady=(0,10))
        tb.Button(toolbar, text="🔄 Recarregar", bootstyle="info", command=self.carregar_alertas).pack(side="left", padx=5)
        tb.Button(toolbar, text="✅ Marcar Resolvido", bootstyle="success", command=self.resolver_alerta).pack(side="left", padx=5)

        # Tabela
        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Produto", "Stock Atual", "Stock Mínimo", "Status", "Data"),
            show="headings", height=15
        )

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

        # tags
        self.tree.tag_configure("ativo", background="#ffdd57")
        self.tree.tag_configure("resolvido", background="#d4edda")

        self.carregar_alertas()

    def _obter_nome_produto(self, produto_id):
        """Método simplificado e mais robusto"""
        try:
            # Tenta o método mais comum primeiro
            produto = self.produto_service.buscar_por_id(produto_id)
            if produto and hasattr(produto, 'nome'):
                return produto.nome
            
            # Fallback: procura em listar_produtos
            if hasattr(self.produto_service, 'listar_produtos'):
                produtos = self.produto_service.listar_produtos()
                for p in produtos:
                    if hasattr(p, 'id_produto') and p.id_produto == produto_id:
                        return getattr(p, 'nome', f"Produto {produto_id}")
        except Exception as e:
            print(f"Erro ao obter nome do produto {produto_id}: {e}")
        
        return f"Produto {produto_id}"

    def carregar_alertas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            alertas = self.service.listar_alertas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar alertas: {e}")
            return

        for a in alertas:
            produto_nome = self._obter_nome_produto(a.produto_id)
            data_str = format_date_safe(a.data_alerta)
            tag = "ativo" if a.status == "ativo" else "resolvido"
            self.tree.insert("", "end", values=(
                a.id_alerta, 
                produto_nome, 
                a.quantidade_atual, 
                a.stock_minimo, 
                a.status, 
                data_str
            ), tags=(tag,))

    def resolver_alerta(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um alerta para marcar como resolvido.")
            return
        
        item = self.tree.item(sel[0])
        id_alerta = item["values"][0]
        
        try:
            ok = self.service.resolver_alerta(id_alerta)
            if ok:
                messagebox.showinfo("Sucesso", "Alerta marcado como resolvido.")
                self.carregar_alertas()
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o alerta.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao resolver alerta: {e}")