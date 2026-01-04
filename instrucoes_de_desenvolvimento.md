## Instruções de Desenvolvimento

### Refatoração Geral e Implementação de Funcionalidades (Concluído)

**Data:** 2026-01-03

**Solicitação:**

Refatorar todo o projeto para alinhar com um novo conjunto de regras e funcionalidades detalhadas, focando em segurança, modularidade e experiência do usuário.

**Resultado:**

- **`main.py`**: Modificado para garantir a verificação e solicitação de privilégios de administrador antes de instanciar a GUI.
- **`utils/admin_check.py`**: Aprimorado com comentários detalhados e lógica de relançamento mais robusta.
- **`ui/app.py`**:
    - Totalmente redesenhado para uma interface mais moderna e funcional.
    - Adicionada uma área de `scrolledtext` para logs em tempo real.
    - Implementado um painel dividido (`PanedWindow`) para separar controles e logs.
    - Funções de módulo agora são chamadas de forma segura através de um wrapper `run_task`.
    - A aba "Inicialização" agora usa uma `Treeview` para listar os programas de forma organizada.
- **`modules/cleaner.py`**:
    - Implementada a limpeza das pastas `%TEMP%` e `C:\Windows\Temp`.
    - Adicionada a função para esvaziar a lixeira (`SHEmptyRecycleBinW`).
    - Melhorado o tratamento de exceções para arquivos em uso.
- **`modules/performance.py`**:
    - Implementada a função para ativar o plano de energia de "Alto Desempenho" via `powercfg`.
    - Implementada a limpeza da pasta `SoftwareDistribution`, incluindo a parada e reinício dos serviços `wuauserv` and `bits`.
- **`modules/startup.py`**: A função `get_startup_apps` foi refinada para ler múltiplas chaves do registro e retornar dados mais estruturados, preparando para futuras interações.
- **`modules/network.py`**:
    - Função `flush_dns` implementada com captura de output e tratamento de erro.
    - Adicionada a função `check_internet_connectivity` usando `socket` para uma verificação rápida.
- **`config/settings.json`**: Atualizado para incluir flags de ativação de funcionalidades e seções para configurações futuras.
- **`README.md`**: Completamente reescrito para incluir o objetivo do projeto, instruções detalhadas de execução, um guia para gerar o `.exe` com PyInstaller e avisos de segurança importantes.
- **Tamanho da Janela**: A janela foi ajustada para 700x600 para acomodar a nova interface com logs.

---

### Ajustes Finais e Funcionalidade de Inicialização (Concluído)

**Data:** 2026-01-03

**Solicitação:**

1.  Remover a tela de console que aparece durante a solicitação de privilégios de administrador.
2.  Adicionar funcionalidade para habilitar/desabilitar programas na aba de "Inicialização".

**Resultado:**

1.  **Remoção do Console:**
    - Em `utils/admin_check.py`, a função `run_as_admin` foi alterada para usar `pythonw.exe` (em vez de `python.exe`) e o parâmetro `nShowCmd` foi definido como `0` (SW_HIDE). Isso garante que o processo de elevação de privilégios ocorra de forma silenciosa, sem nenhuma janela de console.

2.  **Gerenciamento da Inicialização:**
    - **`modules/startup.py`**:
        - Foram adicionadas as funções `enable_startup_app` e `disable_startup_app`.
        - A estratégia implementada é mover as entradas de registro entre `.../Run` e `.../Run_backup`, uma abordagem segura que não apaga as informações.
        - A listagem de apps agora diferencia entre `HKCU` (usuário atual, modificável) e `HKLM` (nível de máquina, somente leitura).
    - **`ui/app.py`**:
        - A aba "Inicialização" foi equipada com os botões "Habilitar Selecionado" e "Desabilitar Selecionado".
        - A `Treeview` foi atualizada para mostrar o status (Habilitado, Desabilitado, Somente Leitura) com cores distintas para fácil identificação.
        - Foram implementadas as lógicas `enable_selected_app` e `disable_selected_app` para conectar os botões às funções do backend e atualizar a lista após a ação.

---

### Remoção da Funcionalidade de Inicialização (Concluído)

**Data:** 2026-01-03

**Solicitação:**

Remover completamente a funcionalidade de gerenciamento de programas de inicialização.

**Resultado:**

- **`ui/app.py`**: A aba "Inicialização" e todos os seus métodos e widgets associados foram removidos da interface. A importação do módulo `startup` também foi removida.
- **`modules/startup.py`**: O arquivo foi tornado órfão. Embora não tenha sido possível deletá-lo via ferramenta, ele não é mais importado ou utilizado pela aplicação.
- **`config/settings.json`**: O flag `enable_startup_manager` foi removido do arquivo de configuração.
- **`README.md`**: A documentação foi atualizada para remover qualquer menção à funcionalidade de gerenciamento da inicialização.

---

### Correção Crítica de Inicialização (Concluído)

**Data:** 2026-01-03

**Solicitação:**

Corrigir a aplicação que não estava abrindo após a remoção da funcionalidade de inicialização.

**Resultado:**

- **Diagnóstico:** A análise revelou que, durante a remoção da aba de inicialização em `ui/app.py`, métodos essenciais (`log`, `run_task`, `create_cleaner_tab`, etc.) foram acidentalmente excluídos. Isso causava um `AttributeError` que impedia a inicialização da aplicação.
- **Correção:** O arquivo `ui/app.py` foi restaurado para um estado correto, contendo todos os métodos necessários para as funcionalidades remanescentes ("Limpeza", "Desempenho", "Rede"), mas excluindo corretamente a funcionalidade de "Inicialização".
- **Status:** A aplicação voltou a funcionar corretamente.

---
### Interface Dinâmica com Blocos (Concluído)

**Data:** 2026-01-04

**Solicitação:**

Criar uma tela dinâmica e minimalista. Em vez de abas, separar as funcionalidades em blocos na tela, cada um com seu próprio ícone.

**Resultado:**

- **`ui/app.py`**: A interface foi totalmente refatorada para substituir o `ttk.Notebook` por um layout de cartões (blocos).
- **Layout**:
    - Três cartões principais foram criados: "Limpeza" (🧹), "Desempenho" (⚡) e "Rede" (🌐).
    - Cada cartão contém um ícone, título, breve descrição e os botões de ação correspondentes.
    - O layout foi organizado horizontalmente, e a janela principal foi alargada para 850px para uma melhor apresentação.
- **Estilo**: Foram adicionados novos estilos para os cartões (`Card.TFrame`) e um cabeçalho principal (`Header.TLabel`) para um visual mais moderno e limpo.
- **Usabilidade**: A nova interface é mais intuitiva, apresentando todas as opções principais diretamente na tela inicial, sem a necessidade de navegar por abas.

---
### Ajuste de Alinhamento (Concluído)

**Data:** 2026-01-04

**Solicitação:**

Ajustar a descrição para ficar centralizada com o quadro.

**Resultado:**

- **`ui/app.py`**: Na função `create_card_frame`, o `ttk.Label` responsável pela descrição foi modificado. As opções `justify` foi alterada para `tk.CENTER` e a âncora do `pack` para `"center"`, garantindo que o texto de descrição em cada cartão seja perfeitamente centralizado.

---
### Atualização do README (Concluído)

**Data:** 2026-01-04

**Solicitação:**

Atualizar todo o arquivo README.md com uma descrição simples e intuitiva do programa, e deixar um comentário no local para colocar uma imagem da tela dele.

**Resultado:**

- **`windows_optimizer/README.md`**: O arquivo foi completamente reescrito para ser mais amigável e direto ao ponto.
- **Conteúdo**: A nova versão inclui uma descrição curta, um placeholder para screenshot, uma lista simplificada de funcionalidades, instruções de uso direto (focadas no executável) e um aviso de responsabilidade.
- **Placeholder de Imagem**: Um comentário `<!-- Insira aqui um screenshot da aplicação -->` e uma tag de imagem `![Windows Optimizer Screenshot](placeholder.png ...)` foram adicionados para facilitar a inserção de uma imagem da interface.

---
### Inserção de Imagem no README (Concluído)

**Data:** 2026-01-04

**Solicitação:**

No campo de imagem, centralize uma imagem específica.

**Resultado:**

- **`windows_optimizer/README.md`**: O placeholder de imagem foi substituído pela tag `<img ...>` fornecida.
- **Centralização**: A imagem foi centralizada envolvendo a tag `<img>` com `<p align="center"> </p>`.
