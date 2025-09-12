import ttkbootstrap as tb
from tkinter import ttk
from services.relatorio_service import RelatorioService
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class RelatoriosView(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.service = RelatorioService()

        self.lbl_title = tb.Label(self, text="Relatórios de Vendas", font=("Arial", 16))
        self.lbl_title.pack(pady=10)

        # Botões de relatórios
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=5)
        self.btn_vendas_dia = tb.Button(btn_frame, text="Vendas Diárias", command=self.vendas_diarias)
        self.btn_vendas_dia.pack(side="left", padx=5)
        self.btn_produtos_vendidos = tb.Button(btn_frame, text="Produtos Mais Vendidos", command=self.produtos_mais_vendidos)
        self.btn_produtos_vendidos.pack(side="left", padx=5)

        # Gráfico
        self.fig, self.ax = plt.subplots(figsize=(6,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Treeview para produtos mais vendidos
        self.tree = ttk.Treeview(self, columns=("Produto ID", "Qtd", "Valor Total"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)
        self.tree.pack_forget()  # escondido inicialmente

    def vendas_diarias(self):
        self.tree.pack_forget()
        self.ax.clear()
        dados = self.service.vendas_por_dia()
        datas = list(dados.keys())
        valores = list(dados.values())
        self.ax.plot(datas, valores, marker='o')
        self.ax.set_title("Vendas Diárias")
        self.ax.set_xlabel("Data")
        self.ax.set_ylabel("Total Vendas")
        self.fig.autofmt_xdate()
        self.canvas.draw()

    def produtos_mais_vendidos(self):
        self.ax.clear()
        self.canvas.draw()
        self.tree.pack(fill="both", expand=True)
        for i in self.tree.get_children():
            self.tree.delete(i)
        produtos = self.service.produtos_mais_vendidos()
        total_geral = sum(p['valor_total'] for p in produtos) or 1
        for p in produtos:
            percentagem = (p['valor_total'] / total_geral) * 100
            self.tree.insert("", "end", values=(p['produto_id'], p['quantidade'], f"{p['valor_total']:.2f} ({percentagem:.1f}%)"))