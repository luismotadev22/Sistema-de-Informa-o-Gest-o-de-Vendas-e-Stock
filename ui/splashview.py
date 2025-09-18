import ttkbootstrap as tb
import tkinter as tk
from dashboard import Dashboard  # Dashboard atualizado com método iniciar()

class SplashScreen(tb.Toplevel):
    def __init__(self, parent, delay=3000):
        super().__init__(parent)
        self.parent = parent
        self.delay = delay
        self.geometry("500x300")
        self.title("Bem-vindo")
        self.overrideredirect(True)
        self.configure(bg="#2c3e50")

        # Centralizar
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        # Conteúdo
        tb.Label(self, text="🛒 Sistema de Gestão", font=("Segoe UI", 20, "bold"),
                 foreground="#ffffff", background="#2c3e50").pack(pady=40)
        tb.Label(self, text="Carregando módulos e dados...", font=("Segoe UI", 12),
                 foreground="#ecf0f1", background="#2c3e50").pack(pady=10)

        # Barra de progresso
        self.progress = tb.Progressbar(self, bootstyle="info-striped", length=400, mode="indeterminate")
        self.progress.pack(pady=30)
        self.progress.start(10)

        # Fechar splash após delay
        self.after(self.delay, self.fechar_splash)

    def fechar_splash(self):
        self.progress.stop()
        self.destroy()
        self.parent.deiconify()  # mostra a janela principal
        # Instancia o Dashboard após splash
        self.parent.dashboard = Dashboard(self.parent)
        self.parent.dashboard.iniciar(aba_inicial="Produtos")  # escolhe aba inicial

# Rodar aplicação
if __name__ == "__main__":
    root = tb.Window(themename="flatly")  # janela principal moderna
    root.withdraw()  # esconde janela principal inicialmente
    splash = SplashScreen(root, delay=3000)
    splash.mainloop()