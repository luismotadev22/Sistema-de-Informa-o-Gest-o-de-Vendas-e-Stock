import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.produto_service import ProdutoService
from models.produto import Produto

class ProdutosView(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.service = ProdutoService()

        self.lbl_title = tb.Label(self, text="Gestão de Produtos", font=("Arial", 16))
        self.lbl_title.pack(pady=10)

        # Treeview
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Nome", "Preço Venda", "Custo Aquisição", "Stock Atual", "Stock Mínimo", "Data Registo"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Botão adicionar produto
        self.btn_add = tb.Button(self, text="Adicionar Produto", bootstyle="success", command=self.adicionar_produto)
        self.btn_add.pack(pady=10)

        self.carregar_produtos()

    def carregar_produtos(self):
        """Limpa e recarrega a Treeview com os produtos."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        for produto in self.service.listar_produtos():
            self.tree.insert(
                "",
                "end",
                values=(
                    produto.id_produto,
                    produto.nome,
                    f"{produto.preco_venda:.2f}",
                    f"{produto.custo_aquisicao:.2f}",
                    produto.stock_atual,
                    produto.stock_minimo,
                    produto.data_registo.strftime("%d/%m/%Y %H:%M:%S") if produto.data_registo else ""
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
        self.title("Adicionar Produto")
        self.result = None
        self.grab_set()

        # Nome
        tb.Label(self, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.nome_entry = tb.Entry(self)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        # Preço de venda
        tb.Label(self, text="Preço Venda:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.preco_entry = tb.Entry(self)
        self.preco_entry.grid(row=1, column=1, padx=10, pady=5)

        # Custo de aquisição
        tb.Label(self, text="Custo Aquisição:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.custo_entry = tb.Entry(self)
        self.custo_entry.grid(row=2, column=1, padx=10, pady=5)

        # Stock atual
        tb.Label(self, text="Stock Atual:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.stock_atual_entry = tb.Entry(self)
        self.stock_atual_entry.grid(row=3, column=1, padx=10, pady=5)

        # Stock mínimo
        tb.Label(self, text="Stock Mínimo:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.stock_minimo_entry = tb.Entry(self)
        self.stock_minimo_entry.grid(row=4, column=1, padx=10, pady=5)

        # Botão Confirmar
        btn = tb.Button(self, text="Confirmar", bootstyle="primary", command=self.confirmar)
        btn.grid(row=5, column=0, columnspan=2, pady=10)

    def confirmar(self):
        try:
            nome = self.nome_entry.get()
            preco_venda = float(self.preco_entry.get())
            custo_aquisicao = float(self.custo_entry.get())
            stock_atual = int(self.stock_atual_entry.get())
            stock_minimo = int(self.stock_minimo_entry.get())

            if not nome:
                raise ValueError("Nome não pode estar vazio.")
            if preco_venda <= 0 or custo_aquisicao <= 0:
                raise ValueError("Valores de preço e custo devem ser positivos.")
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