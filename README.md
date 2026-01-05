# Otimizador de Windows 🚀

Uma ferramenta simples e intuitiva para otimizar e limpar seu sistema Windows com apenas alguns cliques.

<p align="center">
  <img width="424" height="302" alt="image" src="https://github.com/user-attachments/assets/cbece9e2-c3da-4cac-9be4-8a4871599a6c" />
</p>

## ✨ Funcionalidades Principais

O Otimizador de Windows organiza as otimizações em três categorias claras:

- **🧹 Limpeza:** Libere espaço em disco removendo arquivos temporários e esvaziando a lixeira.
- **⚡ Desempenho:** Melhore a velocidade do sistema ativando o plano de energia de "Alto Desempenho" e limpando caches de atualização.
- **🌐 Rede:** Resolva problemas de conectividade limpando o cache DNS e verificando o status da sua conexão.

## 🚀 Como Usar

1.  Execute o arquivo. O aplicativo solicitará permissão de administrador para funcionar corretamente.
2.  Clique nos botões correspondentes às otimizações que você deseja realizar.
3.  Acompanhe o que está acontecendo na área de "Logs de Atividade".

## 📦 Como Gerar o Executável (Para Desenvolvedores)

Se você deseja compilar o aplicativo e criar sua própria release no GitHub, siga os passos abaixo.

### 1. Gerando o `.exe` com PyInstaller

PyInstaller agrupa a aplicação Python em um único arquivo executável.

**a. Instale o PyInstaller:**
```bash
pip install pyinstaller
```

**b. Execute o comando de compilação:**
Navegue até a pasta `windows_optimizer` e execute o seguinte comando:
```bash
pyinstaller --onefile --windowed --name OtimizadorDeWindows main.py
```
- `--onefile`: Cria um único arquivo `.exe`.
- `--windowed`: Evita que uma janela de console apareça ao executar o programa.
- `--name`: Define o nome do executável.

O arquivo `OtimizadorDeWindows.exe` será criado na pasta `dist`.

## ⚠️ Aviso

Este programa faz alterações no seu sistema. Use-o com atenção. Embora seguro, é sempre bom saber o que cada função faz.

---

_Desenvolvido com Python e Tkinter._
