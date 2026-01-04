# -*- coding: utf-8 -*-

"""
Otimizador de Windows
Módulo para otimizações e verificações de rede.
"""

import subprocess
import socket

def flush_dns():
    """
    Executa o comando 'ipconfig /flushdns' para limpar o cache de DNS do sistema.
    Requer privilégios de administrador.

    Retorna:
        list: Logs da operação.
    """
    logs = ["--- Limpando cache de DNS ---"]
    command = "ipconfig /flushdns"
    
    try:
        # A codificação 'cp850' é frequentemente usada para a saída do console do Windows em português.
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding='cp850')
        logs.append("Comando 'ipconfig /flushdns' executado com sucesso.")
        # Adiciona a saída do comando aos logs para confirmação
        output = result.stdout.strip()
        if output:
            logs.append("--- Saída do Comando ---")
            logs.extend(output.splitlines())
            
    except subprocess.CalledProcessError as e:
        logs.append(f"ERRO ao executar o comando: {command}")
        logs.append(f"Código de erro: {e.returncode}")
        # A mensagem de erro em stderr também precisa ser decodificada
        error_message = e.stderr.strip()
        if error_message:
            logs.append(f"Mensagem: {error_message}")
        else:
            logs.append("Ocorreu um erro, mas nenhuma mensagem foi retornada. Verifique as permissões.")
            
    except FileNotFoundError:
        logs.append("ERRO: O comando 'ipconfig' não foi encontrado. Execute em um sistema Windows.")
    except Exception as e:
        logs.append(f"ERRO INESPERADO: {e}")
        
    return logs

def check_internet_connectivity(host="8.8.8.8", port=53, timeout=3):
    """
    Verifica a conectividade com a internet tentando estabelecer uma conexão de socket.
    O padrão é o servidor DNS do Google na porta 53 (DNS).

    Args:
        host (str): O host a ser conectado.
        port (int): A porta a ser usada.
        timeout (int): Tempo em segundos para esperar pela conexão.

    Retorna:
        tuple: (bool, str) indicando o status da conexão e uma mensagem.
    """
    try:
        # Tenta criar um socket e se conectar ao host
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return (True, "Conexão com a internet parece estar ativa.")
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        # Se a conexão falhar, assume-se que não há internet.
        return (False, f"Sem conexão com a internet ou o host está inacessível. Erro: {e}")
    except Exception as e:
        return (False, f"Ocorreu um erro inesperado ao verificar a conexão: {e}")

if __name__ == '__main__':
    # Teste - Requer execução como administrador para flush_dns
    from utils.admin_check import is_admin, run_as_admin
    if not is_admin():
        run_as_admin()

    print("\n--- TESTANDO VERIFICAÇÃO DE CONECTIVIDADE ---")
    is_connected, message = check_internet_connectivity()
    print(f"Status: {'Conectado' if is_connected else 'Desconectado'}")
    print(f"Mensagem: {message}")

    print("\n--- TESTANDO LIMPEZA DE CACHE DNS ---")
    for log in flush_dns():
        print(log)
    
    import os
    os.system("pause")