# -*- coding: utf-8 -*-

"""
Otimizador de Windows
Ponto de entrada principal para a aplicação.

Responsabilidades:
1. Verificar se o script possui privilégios de administrador.
2. Se não possuir, solicitar a elevação através do módulo `admin_check`.
3. Se possuir, inicializar e executar a interface gráfica.
"""

import sys
from ui.app import App
from utils.admin_check import is_admin, run_as_admin

def main():
    """Função principal que inicia o otimizador."""
    
    # Etapa 1: Verificar privilégios
    if not is_admin():
        # Etapa 2: Se não for admin, tenta relançar com privilégios elevados.
        # A função run_as_admin() encerrará este processo se a elevação for bem-sucedida.
        run_as_admin()
        # Se a execução chegar aqui, significa que a elevação falhou ou foi cancelada.
        # O próprio run_as_admin já terá exibido uma mensagem de erro.
        sys.exit(1)

    # Etapa 3: Se o script já é admin, prossegue e cria a janela da aplicação.
    print("Privilégios de administrador confirmados. Iniciando a aplicação...")
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        # Captura de exceção de alto nível para o caso de a GUI falhar ao iniciar.
        print(f"Ocorreu um erro crítico ao iniciar a interface gráfica: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()