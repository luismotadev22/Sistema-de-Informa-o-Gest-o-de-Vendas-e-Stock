import ttkbootstrap as tb
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime
from services.relatorio_service import RelatorioService
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Definir fonte global
rcParams['font.family'] = 'Segoe UI Emoji'

class RelatoriosView(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.service = RelatorioService()
        self.dados_atual = []  # Armazenar dados atuais para exportação
        
        # Configurar para expandir
        self.grid_rowconfigure(3, weight=1)  # Agora linha 3 para o conteúdo
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

        # Botões de Ação (linha 1, continuação)
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

        # NOVO: Botões de Exportação (linha 2)
        export_frame = tb.Frame(self)
        export_frame.grid(row=2, column=0, pady=5, sticky="ew")
        
        self.btn_export_csv = tb.Button(
            export_frame,
            text="💾 Exportar CSV",
            command=self.exportar_csv,
            bootstyle="info-outline",
            width=15,
            state="disabled"  # Inicialmente desativado
        )
        self.btn_export_csv.pack(side="left", padx=5)
        
        self.btn_export_pdf = tb.Button(
            export_frame,
            text="📄 Exportar PDF",
            command=self.exportar_pdf,
            bootstyle="warning-outline",
            width=15,
            state="disabled"  # Inicialmente desativado
        )
        self.btn_export_pdf.pack(side="left", padx=5)
        
        self.btn_limpar = tb.Button(
            export_frame,
            text="🗑️ Limpar",
            command=self.limpar_tudo,
            bootstyle="danger-outline",
            width=15
        )
        self.btn_limpar.pack(side="left", padx=5)

        # Configurar datas automáticas
        self.configurar_datas_automaticas()

        # Área de conteúdo (linha 3) - Notebook para alternar entre gráfico e tabela
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Aba do gráfico
        self.graph_frame = tb.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="📈 Gráfico")
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
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
        
        # Configurar colunas
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
        self.ax.text(
            0.5, 0.5, 
            "Bem-vindo ao Sistema de Relatórios\n\n"
            "📊 Selecione um período e clique em:\n"
            "📈 Vendas Diárias para ver o gráfico\n"
            "📦 Produtos para ver a lista\n\n"
            "💾 Use os botões de exportação para guardar",
            ha='center', va='center', 
            transform=self.ax.transAxes, 
            fontsize=11,
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

    def habilitar_exportacao(self):
        """Habilita os botões de exportação quando há dados"""
        self.btn_export_csv.config(state="normal")
        self.btn_export_pdf.config(state="normal")

    def desabilitar_exportacao(self):
        """Desabilita os botões de exportação quando não há dados"""
        self.btn_export_csv.config(state="disabled")
        self.btn_export_pdf.config(state="disabled")

    def vendas_diarias(self):
        """Exibe gráfico de vendas por dia em euros"""
        try:
            self.notebook.select(0)
            self.ax.clear()

            start_date, end_date = self.get_dates()
            dados = self.service.vendas_por_dia(start_date, end_date)
            
            # Armazenar dados para exportação
            self.dados_atual = {
                'tipo': 'vendas_diarias',
                'dados': dados,
                'periodo': f"{start_date} a {end_date}"
            }
            
            if not dados:
                self.ax.text(0.5, 0.5, "Nenhum dado encontrado", ha='center', va='center', transform=self.ax.transAxes)
                self.ax.set_title("Sem Dados", fontsize=11)
                self.ax.axis('off')
                self.canvas.draw()
                self.desabilitar_exportacao()
                return

            # Processar dados e criar gráfico...
            datas = [venda.dia for venda in dados]
            valores = [venda.total_vendido for venda in dados]
            
            bars = self.ax.bar(range(len(datas)), valores, alpha=0.8, color='#3498db', width=0.6)
            self.ax.set_title(f"Vendas Diárias\nTotal: € {sum(valores):.2f}", fontsize=11)
            self.ax.set_xlabel("Data", fontsize=9)
            self.ax.set_ylabel("Total (€)", fontsize=9)
            self.ax.grid(True, alpha=0.1)
            self.ax.set_xticks(range(len(datas)))
            self.ax.set_xticklabels([d.strftime('%d/%m') for d in datas], rotation=45, fontsize=8)
            
            self.fig.tight_layout()
            self.canvas.draw()
            self.habilitar_exportacao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")
            self.desabilitar_exportacao()

    def produtos_mais_vendidos(self):
        """Exibe produtos mais vendidos com valores em euros"""
        try:
            self.notebook.select(1)

            # Limpar Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)

            start_date, end_date = self.get_dates()
            produtos = self.service.produtos_mais_vendidos(limite=15, start_date=start_date, end_date=end_date)
            
            # Armazenar dados para exportação
            self.dados_atual = {
                'tipo': 'produtos_mais_vendidos',
                'dados': produtos,
                'periodo': f"{start_date} a {end_date}"
            }
            
            if not produtos:
                self.tree.insert("", "end", values=("", "Nenhum produto encontrado", "", ""))
                self.desabilitar_exportacao()
                return

            # Adicionar dados à tabela...
            total_geral = sum(p.valor_total for p in produtos) or 1
            total_quantidade = sum(p.quantidade_total for p in produtos)

            # Cabeçalho
            self.tree.insert("", "end", values=(
                "", f"RELATÓRIO: {len(produtos)} produtos", f"{total_quantidade}", f"€{total_geral:.2f}"
            ), tags=('header',))

            # Dados dos produtos
            for p in produtos:
                self.tree.insert("", "end", values=(
                    p.produto_id,
                    p.nome[:30] + "..." if len(p.nome) > 30 else p.nome,
                    p.quantidade_total,
                    f"€{p.valor_total:.2f}",
                ))

            self.tree.tag_configure('header', background='#e3f2fd', font=('Segoe UI Emoji', 9, 'bold'))
            self.habilitar_exportacao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")
            self.desabilitar_exportacao()

    def exportar_csv(self):
        """Exporta os dados atuais para CSV"""
        if not self.dados_atual or not self.dados_atual['dados']:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar")
            return

        try:
            # Pedir local para salvar
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Salvar relatório como CSV"
            )
            
            if not filename:
                return  # Usuário cancelou

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                if self.dados_atual['tipo'] == 'vendas_diarias':
                    # Cabeçalho para vendas diárias
                    writer.writerow(['Relatório de Vendas Diárias'])
                    writer.writerow(['Período:', self.dados_atual['periodo']])
                    writer.writerow(['Data', 'Total Vendido (€)', 'Número de Vendas'])
                    
                    for venda in self.dados_atual['dados']:
                        writer.writerow([
                            venda.dia.strftime('%d/%m/%Y'),
                            f"{venda.total_vendido:.2f}",
                            venda.num_vendas
                        ])
                        
                elif self.dados_atual['tipo'] == 'produtos_mais_vendidos':
                    # Cabeçalho para produtos mais vendidos
                    writer.writerow(['Relatório de Produtos Mais Vendidos'])
                    writer.writerow(['Período:', self.dados_atual['periodo']])
                    writer.writerow(['ID', 'Produto', 'Quantidade', 'Valor Total (€)'])
                    
                    for produto in self.dados_atual['dados']:
                        writer.writerow([
                            produto.produto_id,
                            produto.nome,
                            produto.quantidade_total,
                            f"{produto.valor_total:.2f}"
                        ])

            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar CSV:\n{str(e)}")

    def exportar_pdf(self):
        """Exporta os dados atuais para PDF"""
        if not self.dados_atual or not self.dados_atual['dados']:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Salvar relatório como PDF"
            )
            
            if not filename:
                return

            # Criar documento PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Título
            titulo = Paragraph(f"<b>Relatório de Vendas</b>", styles['Title'])
            elements.append(titulo)
            elements.append(Spacer(1, 12))
            
            # Período
            periodo = Paragraph(f"<b>Período:</b> {self.dados_atual['periodo']}", styles['Normal'])
            elements.append(periodo)
            elements.append(Spacer(1, 20))
            
            # Dados da tabela
            if self.dados_atual['tipo'] == 'vendas_diarias':
                data = [['Data', 'Total (€)', 'Nº Vendas']]
                for venda in self.dados_atual['dados']:
                    data.append([
                        venda.dia.strftime('%d/%m/%Y'),
                        f"{venda.total_vendido:.2f}",
                        str(venda.num_vendas)
                    ])
                    
            elif self.dados_atual['tipo'] == 'produtos_mais_vendidos':
                data = [['ID', 'Produto', 'Quantidade', 'Total (€)']]
                for produto in self.dados_atual['dados']:
                    data.append([
                        str(produto.produto_id),
                        produto.nome,
                        str(produto.quantidade_total),
                        f"{produto.valor_total:.2f}"
                    ])
            
            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            
            # Rodapé
            elements.append(Spacer(1, 20))
            rodape = Paragraph(f"<i>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</i>", styles['Normal'])
            elements.append(rodape)
            
            # Gerar PDF
            doc.build(elements)
            messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF:\n{str(e)}")

    def limpar_tudo(self):
        """Limpa todos os dados exibidos"""
        self.ax.clear()
        self.mostrar_mensagem_inicial()
        self.canvas.draw()
        
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        self.dados_atual = []
        self.configurar_datas_automaticas()
        self.desabilitar_exportacao()