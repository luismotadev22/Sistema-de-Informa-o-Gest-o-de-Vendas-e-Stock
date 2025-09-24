import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.produto_service import ProdutoService
from models.produto import Produto

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
        tb.Button(toolbar, text="✏️ Editar", bootstyle="warning",
                  command=self.editar_produto).pack(side="left", padx=5)
        tb.Button(toolbar, text="🗑️ Eliminar", bootstyle="danger",
                  command=self.eliminar_produto).pack(side="left", padx=5)
        tb.Button(toolbar, text="🔄 Recarregar", bootstyle="info",
                  command=self.carregar_produtos).pack(side="left", padx=5)

        # 🔹 Tabela
        table_frame = tb.Frame(self)
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame,
                                 columns=("ID", "Nome", "Preço Venda", "Custo Aquisição", "Stock Atual", "Stock Mínimo", "Data Registo"),
                                 show="headings", height=15)
        
        # Configurar colunas
        columns_config = [
            ("ID", 80), ("Nome", 200), ("Preço Venda", 100), 
            ("Custo Aquisição", 120), ("Stock Atual", 100), 
            ("Stock Mínimo", 100), ("Data Registo", 150)
        ]
        
        for col, width in columns_config:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=width, stretch=False)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # 🔹 Bind duplo clique para editar
        self.tree.bind("<Double-1>", lambda e: self.editar_produto())
        
        self.carregar_produtos()

    def carregar_produtos(self):
        """Carrega todos os produtos na tabela"""
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

    def obter_selecao(self):
        """Obtém o item selecionado na tabela"""
        selecao = self.tree.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um produto primeiro.")
            return None
        return selecao[0]

    def adicionar_produto(self):
        """Abre popup para adicionar novo produto"""
        popup = ProdutoPopup(self, titulo="➕ Adicionar Produto")
        self.wait_window(popup)
        if popup.result:
            try:
                produto = Produto(**popup.result)
                produto_id = self.service.adicionar_produto(produto)
                if produto_id:
                    self.carregar_produtos()
                    messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível adicionar o produto.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar produto: {e}")

    def editar_produto(self):
        """Abre popup para editar produto selecionado"""
        item = self.obter_selecao()
        if not item:
            return
            
        valores = self.tree.item(item, "values")
        produto_id = int(valores[0])
        
        # Buscar dados completos do produto
        produto = self.service.obter_por_id(produto_id)
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
            
        popup = ProdutoPopup(self, titulo="✏️ Editar Produto", produto=produto)
        self.wait_window(popup)
        if popup.result:
            try:
                # Atualizar o produto com os novos dados
                produto.nome = popup.result["nome"]
                produto.preco_venda = popup.result["preco_venda"]
                produto.custo_aquisicao = popup.result["custo_aquisicao"]
                produto.stock_atual = popup.result["stock_atual"]
                produto.stock_minimo = popup.result["stock_minimo"]
                
                if self.service.atualizar_produto(produto):
                    self.carregar_produtos()
                    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível atualizar o produto.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")

    def eliminar_produto(self):
        """Elimina o produto selecionado"""
        item = self.obter_selecao()
        if not item:
            return
            
        valores = self.tree.item(item, "values")
        produto_id = int(valores[0])
        produto_nome = valores[1]
        
        # Confirmação de eliminação
        resposta = messagebox.askyesno(
            "Confirmar Eliminação", 
            f"Tem certeza que deseja eliminar o produto '{produto_nome}'?\n\nEsta ação não pode ser desfeita!"
        )
        
        if resposta:
            try:
                if self.service.remover_produto(produto_id):
                    self.carregar_produtos()
                    messagebox.showinfo("Sucesso", "Produto eliminado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível eliminar o produto.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao eliminar produto: {e}")


# -------------------- Popup para Adicionar/Editar Produto --------------------
class ProdutoPopup(tb.Toplevel):
    def __init__(self, master, titulo="Produto", produto=None):
        super().__init__(master)
        self.title(titulo)
        self.result = None
        self.grab_set()
        self.resizable(False, False)
        
        # Centralizar a janela
        self.transient(master)
        self.geometry("+%d+%d" % (master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        
        content = tb.Frame(self, padding=15)
        content.pack(fill="both", expand=True)

        labels = ["Nome:", "Preço Venda (€):", "Custo Aquisição (€):", "Stock Atual:", "Stock Mínimo:"]
        self.entries = {}
        
        for i, label in enumerate(labels):
            tb.Label(content, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tb.Entry(content, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        # Preencher campos se estiver editando
        if produto:
            self.entries["Nome:"].insert(0, produto.nome)
            self.entries["Preço Venda (€):"].insert(0, str(produto.preco_venda))
            self.entries["Custo Aquisição (€):"].insert(0, str(produto.custo_aquisicao))
            self.entries["Stock Atual:"].insert(0, str(produto.stock_atual))
            self.entries["Stock Mínimo:"].insert(0, str(produto.stock_minimo))

        button_frame = tb.Frame(content)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=15)
        
        tb.Button(button_frame, text="Confirmar", bootstyle="primary", 
                 command=self.confirmar).pack(side="left", padx=5)
        tb.Button(button_frame, text="Cancelar", bootstyle="secondary", 
                 command=self.destroy).pack(side="left", padx=5)

        # Bind Enter para confirmar
        self.bind("<Return>", lambda e: self.confirmar())
        self.bind("<Escape>", lambda e: self.destroy())

    def confirmar(self):
        """Valida e confirma os dados do produto"""
        try:
            # Obter e validar dados
            nome = self.entries["Nome:"].get().strip()
            preco_venda_str = self.entries["Preço Venda (€):"].get().replace(',', '.')
            custo_aquisicao_str = self.entries["Custo Aquisição (€):"].get().replace(',', '.')
            stock_atual_str = self.entries["Stock Atual:"].get()
            stock_minimo_str = self.entries["Stock Mínimo:"].get()

            # Validações
            if not nome:
                raise ValueError("Nome não pode estar vazio.")
            
            if not preco_venda_str or not custo_aquisicao_str:
                raise ValueError("Preço e custo são obrigatórios.")
            
            preco_venda = float(preco_venda_str)
            custo_aquisicao = float(custo_aquisicao_str)
            stock_atual = int(stock_atual_str) if stock_atual_str else 0
            stock_minimo = int(stock_minimo_str) if stock_minimo_str else 0

            if preco_venda <= 0 or custo_aquisicao <= 0:
                raise ValueError("Preço e custo devem ser positivos.")
            
            if stock_atual < 0 or stock_minimo < 0:
                raise ValueError("Stock não pode ser negativo.")
            
            if preco_venda < custo_aquisicao:
                raise ValueError("Preço de venda não pode ser menor que o custo de aquisição.")
                
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos: {e}")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro nos dados: {e}")
            return

        # Dados válidos - retornar resultado
        self.result = {
            "nome": nome, 
            "preco_venda": preco_venda, 
            "custo_aquisicao": custo_aquisicao,
            "stock_atual": stock_atual, 
            "stock_minimo": stock_minimo
        }
        self.destroy()