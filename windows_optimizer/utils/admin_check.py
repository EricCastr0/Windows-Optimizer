# -*- coding: utf-8 -*-

"""
Windows Optimizer
Módulo de utilitários para verificação e elevação de privilégios de administrador.
"""

import ctypes
import sys
import os

def is_admin():
    """
    Verifica se o script está sendo executado com privilégios de administrador.

    Retorna:
        bool: True se for administrador, False caso contrário.
    """
    try:
        # A função IsUserAnAdmin() do shell32.dll retorna um valor não-zero se o usuário for admin.
        is_admin_flag = ctypes.windll.shell32.IsUserAnAdmin()
        return is_admin_flag != 0
    except AttributeError:
        # Se a chamada de função falhar (por exemplo, em um sistema não-Windows), assume-se que não é admin.
        return False

def run_as_admin():
    """
    Relança o script atual com privilégios de administrador de forma silenciosa.
    Se a elevação falhar ou for cancelada pelo usuário, o processo atual é encerrado.
    """
    if is_admin():
        return

    # Troca 'python.exe' por 'pythonw.exe' para evitar a abertura de um console
    executable = sys.executable.replace("python.exe", "pythonw.exe")
    
    try:
        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            executable,
            " ".join(sys.argv),
            None,
            0  # nShowCmd = 0 (SW_HIDE) para não mostrar a janela do console
        )
        
        if result > 32:
            sys.exit(0)  # Encerra o processo não-administrativo
        else:
            # A falha na elevação (e.g., usuário clicou em "Não") será silenciosa.
            # O aplicativo simplesmente não vai iniciar. Uma mensagem de erro na GUI
            # no `main.py` antes de chamar `run_as_admin` seria uma boa melhoria.
            sys.exit(1)

    except Exception:
        sys.exit(1)

if __name__ == '__main__':
    if is_admin():
        print("O script está rodando como Administrador.")
        # Simula uma tarefa que precisa de admin
        os.system("pause")
    else:
        print("O script NÃO está rodando como Administrador.")
        run_as_admin()
        # O código abaixo desta linha no else não será executado, pois o script será relançado ou encerrado.
        print("Esta linha não deve ser vista.")