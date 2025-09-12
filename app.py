import ttkbootstrap as tb
from ui.dashboard import Dashboard

def main():
    # Inicializar a aplicação com tema moderno
    root = tb.Window(themename="darkly")  # Pode trocar para 'cosmo', 'flatly', etc.
    root.title("Sistema de Gestão de Vendas e Stock")
    root.geometry("2024x1000")

    # Dashboard principal
    dashboard = Dashboard(root)

    # Executar a aplicação
    root.mainloop()

if __name__ == "__main__":
    main()