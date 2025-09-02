import ttkbootstrap as tb
from ttkbootstrap.constants import *

class Dashboard(tb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("📊 Gestão de Vendas e Stock")
        self.geometry("1000x600")

        # Menu lateral
        menu_frame = tb.Frame(self, bootstyle="secondary")
        menu_frame.pack(side=LEFT, fill=Y)
        tb.Button(menu_frame, text="📦 Produtos", bootstyle="info-outline", command=self.abrir_produtos).pack(fill=X, pady=5, padx=5)
        tb.Button(menu_frame, text="🛒 Vendas", bootstyle="success-outline", command=self.abrir_vendas).pack(fill=X, pady=5, padx=5)
        tb.Button(menu_frame, text="📈 Relatórios", bootstyle="warning-outline", command=self.abrir_relatorios).pack(fill=X, pady=5, padx=5)

        # Área principal
        self.main_frame = tb.Frame(self, bootstyle="light")
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        tb.Label(self.main_frame, text="Bem-vindo ao Sistema!", font=("Segoe UI", 18, "bold"), bootstyle="primary").pack(pady=20)

    def abrir_produtos(self):
        from ui.produtos_view import ProdutosView
        ProdutosView(self.main_frame)

    def abrir_vendas(self):
        from ui.vendas_view import VendasView
        VendasView(self.main_frame)

    def abrir_relatorios(self):
        from ui.relatorios_view import RelatoriosView
        RelatoriosView(self.main_frame)

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()