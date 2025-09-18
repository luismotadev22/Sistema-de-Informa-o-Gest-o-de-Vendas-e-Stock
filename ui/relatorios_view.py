import ttkbootstrap as tb
from tkinter import ttk, messagebox
from services.relatorio_service import RelatorioService
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
from datetime import datetime

# Definir fonte global com suporte a emojis
rcParams['font.family'] = 'Segoe UI Emoji'  # Windows



class RelatoriosView(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.service = RelatorioService()
        
        # Configurar para expandir
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Título (linha 0)
        self.lbl_title = tb.Label(
            self, 
            text="📊 Relatórios de Vendas", 
            font=('Segoe UI Emoji', 14, 'bold'),
            foreground='#2c3e50'
        )
        self.lbl_title.grid(row=0, column=0, pady=10, sticky="ew")

        # Filtros (linha 1)
        filter_frame = tb.Frame(self)
        filter_frame.grid(row=1, column=0, pady=10, sticky="ew")
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(3, weight=1)

        tb.Label(filter_frame, text="Data Início:", font=('Segoe UI Emoji', 9)).grid(row=0, column=0, padx=5, sticky="w")
        self.entry_start_date = tb.Entry(filter_frame, width=12, font=('Segoe UI Emoji', 9))
        self.entry_start_date.grid(row=0, column=1, padx=5, sticky="w")

        tb.Label(filter_frame, text="Data Fim:", font=('Segoe UI Emoji', 9)).grid(row=0, column=2, padx=5, sticky="w")
        self.entry_end_date = tb.Entry(filter_frame, width=12, font=('Segoe UI Emoji', 9))
        self.entry_end_date.grid(row=0, column=3, padx=5, sticky="w")

        # Botões (linha 1, continuação)
        self.btn_vendas_dia = tb.Button(
            filter_frame, 
            text="📈 Vendas Diárias", 
            command=self.vendas_diarias,
            bootstyle="success-outline",
            width=15
        )
        self.btn_vendas_dia.grid(row=0, column=4, padx=5)

        self.btn_produtos_vendidos = tb.Button(
            filter_frame, 
            text="📦 Produtos", 
            command=self.produtos_mais_vendidos,
            bootstyle="primary-outline",
            width=15
        )
        self.btn_produtos_vendidos.grid(row=0, column=5, padx=5)

        # Configurar datas automáticas
        self.configurar_datas_automaticas()

        # Área de conteúdo (linha 2) - Notebook para alternar entre gráfico e tabela
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Aba do gráfico
        self.graph_frame = tb.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="📈 Gráfico")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))  # Tamanho menor
        self.fig.patch.set_facecolor('#f8f9fa')
        self.ax.set_facecolor('#ffffff')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Aba da tabela
        self.table_frame = tb.Frame(self.notebook)
        self.notebook.add(self.table_frame, text="📦 Produtos")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Treeview para produtos mais vendidos
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("ID", "Produto", "Quantidade", "Valor"),
            show="headings",
            height=15
        )
        
        # Configurar headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Quantidade", text="Qtd")
        self.tree.heading("Valor", text="Valor (€)")
        
        # Configurar colunas (mais estreitas)
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Produto", width=150, anchor="w")
        self.tree.column("Quantidade", width=60, anchor="center")
        self.tree.column("Valor", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Mensagem inicial
        self.mostrar_mensagem_inicial()

    def configurar_datas_automaticas(self):
        """Configura automaticamente as datas para o ano atual"""
        ano_atual = datetime.now().year
        data_inicio = f"{ano_atual}-01-01"
        data_fim = f"{ano_atual}-12-31"
        
        self.entry_start_date.delete(0, 'end')
        self.entry_end_date.delete(0, 'end')
        self.entry_start_date.insert(0, data_inicio)
        self.entry_end_date.insert(0, data_fim)

    def mostrar_mensagem_inicial(self):
        """Mostra mensagem inicial no gráfico"""
        self.ax.clear()
        self.fig.set_size_inches(8, 6) 
        self.ax.text(
            0.5, 0.5, 
            "Bem-vindo ao Sistema de Relatórios\n\n"
            "📊 Selecione um período e clique em:\n"
            "📈 Vendas Diárias para ver o gráfico\n"
            "📦 Produtos para ver a lista\n\n"
            "💡 Use datas no formato AAAA-MM-DD",
            ha='center', va='center', 
            transform=self.ax.transAxes, 
            fontsize=13,
            bbox=dict(boxstyle="round,pad=1", facecolor="#e3f2fd", edgecolor="#bbdefb")
        )
        self.ax.set_title("Sistema de Relatórios", fontsize=14, pad=20)
        self.ax.axis('off')
        self.canvas.draw()

    def get_dates(self):
        """Obtém as datas dos filtros"""
        start_date = self.entry_start_date.get().strip() or None
        end_date = self.entry_end_date.get().strip() or None
        return start_date, end_date

    def vendas_diarias(self):
        """Exibe gráfico de vendas por dia em euros"""
        try:
            self.notebook.select(0)  # Seleciona aba do gráfico
            self.ax.clear()

            start_date, end_date = self.get_dates()
            dados = self.service.vendas_por_dia(start_date, end_date)
            
            if not dados:
                self.ax.text(
                    0.5, 0.5, 
                    "Nenhum dado encontrado\n\n"
                    "Verifique:\n"
                    "• Datas informadas\n"
                    "• Vendas no período\n"
                    "• Conexão com BD", 
                    ha='center', va='center', 
                    transform=self.ax.transAxes, 
                    fontsize=9
                )
                self.ax.set_title("Sem Dados", fontsize=11)
                self.ax.axis('off')
                self.canvas.draw()
                return

            # Processar dados
            datas = [venda.dia for venda in dados]
            valores = [venda.total_vendido for venda in dados]
            num_vendas = [venda.num_vendas for venda in dados]

            # Criar gráfico mais simples
            bars = self.ax.bar(range(len(datas)), valores, alpha=0.8, color='#3498db', width=0.6)
            self.ax.set_title(f"Vendas Diárias\nTotal: € {sum(valores):.2f}", fontsize=11)
            self.ax.set_xlabel("Data", fontsize=9)
            self.ax.set_ylabel("Total (€)", fontsize=9)
            self.ax.grid(True, alpha=0.1)
            
            # Configurar eixos
            self.ax.set_xticks(range(len(datas)))
            self.ax.set_xticklabels([d.strftime('%d/%m') for d in datas], rotation=45, fontsize=8)
            self.ax.tick_params(axis='y', labelsize=8)
            
            # Adicionar valores apenas se espaço suficiente
            if len(datas) <= 10:  # Só mostra valores se poucos dias
                for bar, valor in zip(bars, valores):
                    if valor > 0:
                        self.ax.text(
                            bar.get_x() + bar.get_width()/2., 
                            valor + max(valores)*0.02,
                            f'€{valor:.0f}', 
                            ha='center', 
                            va='bottom', 
                            fontsize=7
                        )

            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")

    def produtos_mais_vendidos(self):
        """Exibe produtos mais vendidos com valores em euros"""
        try:
            self.notebook.select(1)  # Seleciona aba da tabela

            # Limpar Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)

            start_date, end_date = self.get_dates()
            produtos = self.service.produtos_mais_vendidos(limite=15, start_date=start_date, end_date=end_date)
            
            if not produtos:
                self.tree.insert("", "end", values=("", "Nenhum produto encontrado", "", ""))
                return

            # Calcular totais
            total_geral = sum(p.valor_total for p in produtos) or 1
            total_quantidade = sum(p.quantidade_total for p in produtos)

            # Cabeçalho
            self.tree.insert("", "end", values=(
                "", 
                f"RELATÓRIO: {len(produtos)} produtos", 
                f"{total_quantidade}", 
                f"€{total_geral:.2f}"
            ), tags=('header',))

            # Dados dos produtos
            for p in produtos:
                percentagem = (p.valor_total / total_geral) * 100
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        p.produto_id,
                        p.nome[:30] + "..." if len(p.nome) > 30 else p.nome,  # Limitar tamanho
                        p.quantidade_total,
                        f"€{p.valor_total:.2f}",
                    ),
                )

            # Configurar estilo do header
            self.tree.tag_configure('header', background='#e3f2fd', font=('Segoe UI Emoji', 9, 'bold'))
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")

    def limpar_tudo(self):
        """Limpa todos os dados exibidos"""
        self.ax.clear()
        self.mostrar_mensagem_inicial()
        self.canvas.draw()
        
        for i in self.tree.get_children():
            self.tree.delete(i)
              
        self.configurar_datas_automaticas()
