# -*- coding: utf-8 -*-

"""
Otimizador de Windows
Módulo para otimizações de desempenho do sistema.
"""

import subprocess
import shutil
import os

def set_high_performance_power_plan():
    """
    Ativa o plano de energia de "Alto Desempenho" do Windows.
    Requer privilégios de administrador.

    Retorna:
        list: Logs da operação.
    """
    logs = ["--- Ativando plano de energia 'Alto Desempenho' ---"]
    high_performance_guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    command = f"powercfg /setactive {high_performance_guid}"
    
    try:
        # Executa o comando para ativar o plano de energia
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding='cp850')
        logs.append("Plano de energia 'Alto Desempenho' ativado com sucesso.")
        if result.stdout:
            logs.append(f"Saída do comando: {result.stdout.strip()}")
            
    except subprocess.CalledProcessError as e:
        logs.append(f"ERRO ao executar o comando: {command}")
        logs.append(f"Código de erro: {e.returncode}")
        logs.append(f"Mensagem: {e.stderr.strip()}")
    except FileNotFoundError:
        logs.append("ERRO: O comando 'powercfg' não foi encontrado. Este script deve ser executado no Windows.")
    except Exception as e:
        logs.append(f"ERRO INESPERADO: {e}")
        
    return logs

def clean_softwaredistribution_folder():
    """
    Limpa o conteúdo da pasta C:\Windows\SoftwareDistribution\Download.
    Esta pasta armazena arquivos de instalação do Windows Update.
    Requer privilégios de administrador para parar/iniciar o serviço wuauserv.

    Retorna:
        list: Logs da operação.
    """
    logs = ["--- Limpando cache de atualizações do Windows (SoftwareDistribution) ---"]
    folder_path = r"C:\Windows\SoftwareDistribution\Download"
    
    commands_stop = [
        "net stop wuauserv",
        "net stop bits"
    ]
    commands_start = [
        "net start wuauserv",
        "net start bits"
    ]

    def run_service_commands(commands):
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                logs.append(f"Comando executado com sucesso: {cmd}")
            except subprocess.CalledProcessError as e:
                logs.append(f"AVISO: Falha ao executar '{cmd}'. Motivo: {e.stderr.strip()}")

    logs.append("Parando serviços do Windows Update...")
    run_service_commands(commands_stop)

    logs.append(f"Limpando o diretório: {folder_path}")
    if os.path.isdir(folder_path):
        for item in os.listdir(folder_path):
            full_path = os.path.join(folder_path, item)
            try:
                if os.path.isfile(full_path) or os.path.islink(full_path):
                    os.unlink(full_path)
                    logs.append(f"Arquivo removido: {full_path}")
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    logs.append(f"Diretório removido: {full_path}")
            except (PermissionError, OSError) as e:
                logs.append(f"ERRO: Não foi possível remover {full_path}. Motivo: {e}")
    else:
        logs.append(f"AVISO: Diretório não encontrado: {folder_path}")

    logs.append("Iniciando serviços do Windows Update...")
    run_service_commands(commands_start)
    
    logs.append("--- Limpeza do cache de atualizações concluída. ---")
    return logs

if __name__ == '__main__':
    # Teste - Requer execução como administrador
    from utils.admin_check import is_admin, run_as_admin
    if not is_admin():
        run_as_admin()

    print("\n--- TESTANDO PLANO DE ENERGIA ---")
    for log in set_high_performance_power_plan():
        print(log)

    print("\n--- TESTANDO LIMPEZA DE SOFTWAREDISTRIBUTION ---")
    for log in clean_softwaredistribution_folder():
        print(log)
    
    os.system("pause")