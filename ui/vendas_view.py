import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.venda_service import VendaService
from services.produto_service import ProdutoService


class VendasView(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.service = VendaService()
        self.produto_service = ProdutoService()

        self.lbl_title = tb.Label(self, text="Gestão de Vendas", font=("Arial", 16))
        self.lbl_title.pack(pady=10)

        # Treeview
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Produto ID", "Nome Produto", "Qtd", "Preço Unit.", "Total", "Data"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Botão adicionar venda
        self.btn_add = tb.Button(self, text="Registrar Venda", bootstyle="success", command=self.adicionar_venda)
        self.btn_add.pack(pady=10)

        self.carregar_vendas()

    def carregar_vendas(self):
        """Limpa e recarrega a Treeview com as vendas."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for venda in self.service.listar_vendas():
            produto = self.produto_service.obter_por_id(venda.produto_id)
            nome_produto = produto.nome if produto else "Desconhecido"
            self.tree.insert(
                "",
                "end",
                values=(
                    venda.id_venda,
                    venda.produto_id,
                    nome_produto,
                    venda.quantidade,
                    f"{venda.preco_unitario:.2f}",
                    f"{venda.total:.2f}",
                    venda.data_venda.strftime("%d/%m/%Y %H:%M:%S") if venda.data_venda else ""
                )
            )

    def adicionar_venda(self):
        """Popup para registrar uma nova venda."""
        popup = VendaPopup(self)
        self.wait_window(popup)
        if popup.result:
            produto_id, quantidade, preco_unitario = popup.result
            self.service.registar_venda(produto_id, quantidade, preco_unitario)  # nome corrigido
            self.carregar_vendas()

    def mostrar_relatorio_vendas(self):
        """Mostra relatório de vendas diárias no console."""
        relatorio = self.service.vendas_diarias()
        for linha in relatorio:
            print(f"Dia: {linha['dia']} | Total vendido: {linha['total_vendido']} | Nº vendas: {linha['num_vendas']}")

    def mostrar_produtos_mais_vendidos(self):
        """Mostra relatório dos produtos mais vendidos no console."""
        top = self.service.produtos_mais_vendidos()
        for p in top:
            print(f"{p['nome']} - {p['quantidade_total']} unidades - €{p['valor_total']}")


class VendaPopup(tb.Toplevel):
    """Popup para registrar venda."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Registrar Venda")
        self.result = None
        self.grab_set()

        self.produto_service = ProdutoService()

        # Produto (combobox com nomes dos produtos)
        tb.Label(self, text="Produto:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.produtos = self.produto_service.listar_produtos()
        self.produto_var = tb.StringVar()
        self.produto_combo = ttk.Combobox(
            self,
            textvariable=self.produto_var,
            values=[f"{p.id_produto} - {p.nome}" for p in self.produtos],
            state="readonly"
        )
        self.produto_combo.grid(row=0, column=1, padx=10, pady=5)

        # Quantidade
        tb.Label(self, text="Quantidade:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.quantidade_entry = tb.Entry(self)
        self.quantidade_entry.grid(row=1, column=1, padx=10, pady=5)

        # Preço Unitário
        tb.Label(self, text="Preço Unitário:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.preco_entry = tb.Entry(self)
        self.preco_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botão Confirmar
        btn = tb.Button(self, text="Confirmar", bootstyle="primary", command=self.confirmar)
        btn.grid(row=3, column=0, columnspan=2, pady=10)

    def confirmar(self):
        try:
            produto_str = self.produto_var.get()
            if not produto_str:
                raise ValueError("Selecione um produto.")
            produto_id = int(produto_str.split(" - ")[0])  # pega o id_produto
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