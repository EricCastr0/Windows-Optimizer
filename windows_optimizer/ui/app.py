# -*- coding: utf-8 -*-

"""
Windows Optimizer
Módulo principal da interface gráfica (GUI) construído com Tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, PanedWindow
from functools import partial

# Importando os módulos de funcionalidade
from modules import cleaner, performance, network
from utils.admin_check import is_admin

class App(tk.Tk):
    """Janela principal da aplicação."""

    def __init__(self):
        super().__init__()

        if not is_admin():
            messagebox.showerror("Erro de Permissão", "Este aplicativo precisa ser executado com privilégios de administrador.")
            self.destroy()
            return

        self.title("Windows Optimizer")
        self.configure_window()
        self.create_widgets()

    def configure_window(self):
        """Configura o tamanho e a posição da janela."""
        window_width = 850
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.minsize(850, 600)

    def create_widgets(self):
        """Cria e organiza os widgets na janela."""
        # --- Estilo ---
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Segoe UI', 10))
        style.configure("TLabel", font=('Segoe UI', 11))
        style.configure("Title.TLabel", font=('Segoe UI', 14, 'bold'))
        style.configure("Header.TLabel", font=('Segoe UI', 18, 'bold'))
        style.configure("Card.TFrame", relief="solid", borderwidth=1, padding=15)

        # --- Painel principal dividido ---
        main_pane = PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        main_pane.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(main_pane, padding="10")
        self.log_area_frame = ttk.Frame(main_pane, padding="5")
        main_pane.add(top_frame, height=380) # Aumentar altura para os cartões
        main_pane.add(self.log_area_frame)
        
        # --- Área de Logs ---
        log_label = ttk.Label(self.log_area_frame, text="Logs de Atividade", style="Title.TLabel")
        log_label.pack(pady=(5, 10), anchor="w")
        self.log_text = scrolledtext.ScrolledText(self.log_area_frame, wrap=tk.WORD, font=("Consolas", 9), state="disabled", background="#f0f0f0")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # --- Título Principal ---
        header_label = ttk.Label(top_frame, text="Otimizador de Desempenho", style="Header.TLabel", anchor="center")
        header_label.pack(fill=tk.X, pady=(10, 20))

        # --- Container para os cartões ---
        cards_container = ttk.Frame(top_frame)
        cards_container.pack(fill=tk.BOTH, expand=True)

        # --- Criação dos Blocos/Cartões ---
        self.create_cleaner_card(cards_container)
        self.create_performance_card(cards_container)
        self.create_network_card(cards_container)

    def log(self, messages):
        """Adiciona mensagens à área de logs."""
        self.log_text.config(state="normal")
        if isinstance(messages, list):
            for msg in messages:
                self.log_text.insert(tk.END, msg + "\n")
        else:
            self.log_text.insert(tk.END, messages + "\n")
        self.log_text.see(tk.END) # Auto-scroll
        self.log_text.config(state="disabled")

    def run_task(self, task_function, *args):
        """Executa uma função de módulo e loga os resultados."""
        self.log(f"🚀 Iniciando tarefa: {task_function.__name__}...")
        try:
            results = task_function(*args)
            if results:
                self.log(results)
            self.log(f"✅ Tarefa '{task_function.__name__}' concluída com sucesso!")
        except Exception as e:
            self.log(f"❌ ERRO na tarefa '{task_function.__name__}': {e}")
            messagebox.showerror("Erro de Execução", f"Ocorreu um erro inesperado:\n{e}")
        self.log("-" * 50)

    def create_card_frame(self, parent, title_text, description_text, icon):
        """Cria um frame estilizado para uma categoria de otimização."""
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        header_frame = ttk.Frame(card)
        header_frame.pack(fill=tk.X, anchor="w")

        ttk.Label(header_frame, text=icon, font=('Segoe UI', 24)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(header_frame, text=title_text, style="Title.TLabel").pack(side=tk.LEFT, anchor="w")

        ttk.Label(card, text=description_text, wraplength=200, justify=tk.CENTER).pack(anchor="center", pady=(10, 15))
        
        # Frame para os botões, para que eles fiquem na parte de baixo
        button_frame = ttk.Frame(card)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))

        return button_frame

    # --- BLOCO DE LIMPEZA ---
    def create_cleaner_card(self, parent):
        button_frame = self.create_card_frame(
            parent,
            title_text="Limpeza",
            description_text="Remove arquivos temporários e desnecessários do sistema para liberar espaço em disco.",
            icon="🧹"
        )
        
        btn_temp = ttk.Button(button_frame, text="Limpar Pastas Temporárias", command=partial(self.run_task, cleaner.clean_temp_folders))
        btn_temp.pack(fill=tk.X, pady=5)
        
        btn_recycle = ttk.Button(button_frame, text="Esvaziar Lixeira", command=partial(self.run_task, cleaner.empty_recycle_bin))
        btn_recycle.pack(fill=tk.X, pady=5)

    # --- BLOCO DE DESEMPENHO ---
    def create_performance_card(self, parent):
        button_frame = self.create_card_frame(
            parent,
            title_text="Desempenho",
            description_text="Aplica configurações para melhorar a performance e a velocidade geral do sistema.",
            icon="⚡"
        )
        
        btn_power_plan = ttk.Button(button_frame, text="Ativar Alto Desempenho", command=partial(self.run_task, performance.set_high_performance_power_plan))
        btn_power_plan.pack(fill=tk.X, pady=5)
        
        btn_soft_dist = ttk.Button(button_frame, text="Limpar Cache de Updates", command=partial(self.run_task, performance.clean_softwaredistribution_folder))
        btn_soft_dist.pack(fill=tk.X, pady=5)

    # --- BLOCO DE REDE ---
    def create_network_card(self, parent):
        button_frame = self.create_card_frame(
            parent,
            title_text="Rede",
            description_text="Realiza otimizações para melhorar a conectividade e resolver problemas comuns de rede.",
            icon="🌐"
        )
        
        btn_dns = ttk.Button(button_frame, text="Limpar Cache DNS", command=partial(self.run_task, network.flush_dns))
        btn_dns.pack(fill=tk.X, pady=5)
        
        btn_check_conn = ttk.Button(button_frame, text="Verificar Conexão", command=self.check_connectivity)
        btn_check_conn.pack(fill=tk.X, pady=5)

    def check_connectivity(self):
        """Função específica para o botão de verificação de conexão."""
        self.log("📡 Verificando conexão com a internet...")
        is_connected, message = network.check_internet_connectivity()
        self.log(message)
        if is_connected:
            messagebox.showinfo("Status da Conexão", message)
        else:
            messagebox.showwarning("Status da Conexão", message)
        self.log("-" * 50)


if __name__ == "__main__":
    # Simula a execução a partir do main.py
    if is_admin():
        app = App()
        app.mainloop()
    else:
        # No teste direto, apenas informa. O main.py real cuidará de relançar.
        print("Este script precisa de privilégios de administrador para funcionar corretamente.")
        # Em um cenário real, main.py chamaria run_as_admin() antes de instanciar a App.
        # Ex:
        # from utils.admin_check import run_as_admin
        # run_as_admin()
        # app = App()
        # app.mainloop()
