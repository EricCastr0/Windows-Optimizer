# -*- coding: utf-8 -*-

"""
Windows Optimizer
Módulo para gerenciamento de programas que iniciam com o Windows.
"""

import winreg

# Chave de registro para programas de inicialização do usuário atual
RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
# Subchave para "desativar" programas de inicialização (uma prática comum e segura)
DISABLED_RUN_KEY_PATH = RUN_KEY_PATH + "_backup"

def get_startup_apps():
    """
    Lista os programas configurados para iniciar com o Windows para o usuário atual.
    Verifica tanto os habilitados (na chave 'Run') quanto os desabilitados (na chave 'Run_backup').

    Retorna:
        list: Uma lista de dicionários, cada um representando um programa.
    """
    apps = []
    # Mapeamento Hive -> String
    hkey_map = {
        "enabled": (winreg.HKEY_CURRENT_USER, RUN_KEY_PATH),
        "disabled": (winreg.HKEY_CURRENT_USER, DISABLED_RUN_KEY_PATH)
    }

    for status, (hkey, subkey_path) in hkey_map.items():
        try:
            with winreg.OpenKey(hkey, subkey_path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        apps.append({
                            "name": name,
                            "path": value,
                            "enabled": status == "enabled",
                            "location": "HKCU" # Focando no usuário atual por segurança
                        })
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            # É normal a chave de backup não existir inicialmente
            continue
        except Exception as e:
            print(f"Erro ao ler o registro: {e}") # Log de erro
            
    # Adicionar HKLM (somente leitura)
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RUN_KEY_PATH, 0, winreg.KEY_READ) as key:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    apps.append({
                        "name": name,
                        "path": value,
                        "enabled": True,
                        "location": "HKLM (Read-Only)"
                    })
                    i += 1
                except OSError:
                    break
    except FileNotFoundError:
        pass # Normal
    except Exception as e:
        print(f"Erro ao ler HKLM: {e}")

    return apps

def _move_registry_key(app_name, from_path, to_path):
    """Função auxiliar para mover um valor entre chaves de registro."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, from_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as from_key:
            # 1. Ler o valor da chave de origem
            value, type = winreg.QueryValueEx(from_key, app_name)
            
            # 2. Criar/abrir a chave de destino e escrever o valor
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, to_path) as to_key:
                winreg.SetValueEx(to_key, app_name, 0, type, value)
            
            # 3. Deletar o valor da chave de origem
            winreg.DeleteValue(from_key, app_name)
            return True, f"'{app_name}' movido de '{from_path}' para '{to_path}'."
            
    except FileNotFoundError:
        return False, "Chave de origem ou '" + app_name + "' não encontrado."
    except PermissionError:
        return False, "Permissão negada para modificar o registro."
    except Exception as e:
        return False, f"Erro inesperado no registro: {e}"


def disable_startup_app(app_name):
    """
    Desabilita um programa de inicialização movendo-o para a chave de backup.
    Funciona apenas para chaves do usuário atual (HKCU).
    """
    if not app_name:
        return False, "Nenhum aplicativo selecionado."
    return _move_registry_key(app_name, RUN_KEY_PATH, DISABLED_RUN_KEY_PATH)

def enable_startup_app(app_name):
    """
    Habilita um programa de inicialização movendo-o da chave de backup para a chave 'Run'.
    Funciona apenas para chaves do usuário atual (HKCU).
    """
    if not app_name:
        return False, "Nenhum aplicativo selecionado."
    return _move_registry_key(app_name, DISABLED_RUN_KEY_PATH, RUN_KEY_PATH)


if __name__ == "__main__":
    # Teste
    all_apps = get_startup_apps()
    print("--- Programas de Inicialização Encontrados ---")
    for app in all_apps:
        print(f"- {app['name']} (Habilitado: {app['enabled']}, Local: {app['location']})")

    # Para testar, pegue um nome de app da lista e descomente as linhas abaixo
    # app_to_toggle = "NOME_DO_APP_AQUI" 
    
    # if any(app['name'] == app_to_toggle and app['enabled'] for app in all_apps):
    #     print(f"\n--- Tentando desabilitar '{app_to_toggle}' ---")
    #     success, message = disable_startup_app(app_to_toggle)
    #     print(message)
    # else:
    #     print(f"\n--- Tentando habilitar '{app_to_toggle}' ---")
    #     success, message = enable_startup_app(app_to_toggle)
    #     print(message)
    
    # print("\n--- Lista Atualizada ---")
    # for app in get_startup_apps():
    #     print(f"- {app['name']} (Habilitado: {app['enabled']})")
        
    import os
    os.system("pause")
