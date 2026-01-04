# -*- coding: utf-8 -*-

"""
Otimizador de Windows
Módulo para limpeza de arquivos do sistema.
"""

import os
import shutil
import tempfile
import ctypes

def clean_temp_folders():
    """
    Limpa as pastas de arquivos temporários do Windows e do usuário.
    - C:\\Windows\\Temp
    - %TEMP% (variável de ambiente)

    Retorna:
        list: Uma lista de logs das ações executadas.
    """
    logs = []
    # Lista de diretórios a serem limpos
    temp_dirs = [tempfile.gettempdir(), r"C:\\Windows\\Temp"]
    
    for directory in temp_dirs:
        logs.append(f"--- Limpando o diretório: {directory} ---")
        if not os.path.isdir(directory):
            logs.append(f"AVISO: Diretório não encontrado: {directory}")
            continue
            
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            try:
                if os.path.isfile(full_path) or os.path.islink(full_path):
                    os.unlink(full_path)
                    logs.append(f"Arquivo removido: {full_path}")
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    logs.append(f"Diretório removido: {full_path}")
            except (PermissionError, OSError) as e:
                # Arquivos em uso ou protegidos pelo sistema não podem ser removidos.
                logs.append(f"ERRO: Não foi possível remover {full_path}. Motivo: {e}")
            except Exception as e:
                logs.append(f"ERRO INESPERADO: {full_path}. Motivo: {e}")
                
    logs.append("--- Limpeza de pastas temporárias concluída. ---")
    return logs

def empty_recycle_bin():
    """
    Esvazia a lixeira do Windows para todos os drives.
    Requer privilégios de administrador.

    Retorna:
        list: Uma lista de logs da ação.
    """
    logs = ["--- Tentando esvaziar a lixeira... ---"]
    try:
        # A função SHEmptyRecycleBin do shell32.dll esvazia a lixeira.
        # O primeiro argumento é o handle da janela (pode ser None).
        # O segundo é o drive (None para todos).
        # O terceiro são flags (0x00000001 para não mostrar progresso, 0x00000002 para não pedir confirmação).
        flags = 0x00000001 | 0x00000002
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
        
        if result == 0: # S_OK
            logs.append("Lixeira esvaziada com sucesso.")
        else:
            logs.append(f"ERRO: Falha ao esvaziar a lixeira (Código: {result}).")
            
    except Exception as e:
        logs.append(f"ERRO INESPERADO ao tentar esvaziar a lixeira: {e}")
        
    return logs

if __name__ == "__main__":
    # Teste - Requer execução como administrador
    from utils.admin_check import is_admin, run_as_admin
    if not is_admin():
        run_as_admin()

    print("\n--- INICIANDO LIMPEZA DE PASTAS TEMP ---")
    for log_message in clean_temp_folders():
        print(log_message)

    print("\n--- INICIANDO LIMPEZA DA LIXEIRA ---")
    for log_message in empty_recycle_bin():
        print(log_message)
        
    os.system("pause")