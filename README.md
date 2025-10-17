# google-cloud-agent-demo

## Passo a Passo para rodar os demos do ADK
* Acessar esse repo: https://github.com/fmsedrez/google-cloud-agent-demo/
* Acessar o site: https://shell.cloud.google.com/
* Instalar o UV:
  * No terminal do Google Cloud Shell, digitar:
  * curl -LsSf https://astral.sh/uv/install.sh | sh
  * source $HOME/.local/bin/env
  * uv --version
* Atualizar o UV (se já estiver instalado):
  * No terminal do Google Cloud Shell, digitar:
  * uv self update
  * uv --version
* Atualizar pacotes do projeto (se já estiver instalado):
  * No terminal do Google Cloud Shell, digitar:
  * uv sync --upgrade
* Definir o projeto do Google Cloud:
  * No terminal digitar: `gcloud config set project <ID_DO_PROJETO>`
* Certifique-se que a API do Vertex AI está ativada no seu projeto do Google Cloud.
  * Usando o gcloud CLI, você pode ativar a API com o seguinte comando:
    * `gcloud services enable aiplatform.googleapis.com`
    * `gcloud services enable geminidataanalytics.googleapis.com`
* Garantir que você tem uma conta no Google Cloud com permissão de acessar e usar o projeto.
  * São os seguintes papéis para o usuário:
    * `roles/serviceusage.serviceUsageConsumer`
    * `roles/aiplatform.user`
    * `roles/bigquery.user` (se for usar BigQuery)
    * Usando os commandos: 
      * gcloud projects add-iam-policy-binding <ID_DO_PROJETO> --member='user:<SEU_EMAIL>' --role='roles/aiplatform.user'
      * gcloud projects add-iam-policy-binding <ID_DO_PROJETO> --member='user:<SEU_EMAIL>' --role='roles/serviceusage.serviceUsageConsumer'
      * gcloud projects add-iam-policy-binding <ID_DO_PROJETO> --member='user:<SEU_EMAIL>' --role='roles/bigquery.user'
* Ativar a conta padrão do Google Cloud Shell:
  * No terminal digitar: `gcloud auth application-default login --no-launch-browser`
* Criar o ambiente virtual:
  * `make venv`
* Baixar as dependências do projeto:
  * `make sync`
* Instalar esse projeto:
  * No terminal digitar: `uv install -e .`
* Configurar variáveis de ambiente:
  * `uv run setenv`
  * eval $(uv run setenv --export)

## Comentários e melhorias sugeridas

Estas são sugestões para tornar o passo a passo mais completo e fácil de seguir. Não alteram o fluxo atual, apenas complementam com alternativas, verificações e como executar os demos.

- Pré‑requisitos e papéis (IAM)
  - Confirme se os papéis listados são suficientes para seu caso de uso. Em muitos cenários de Vertex AI, os papéis abaixo atendem:
    - roles/serviceusage.serviceUsageConsumer
    - roles/aiplatform.user
  - Se você encontrará recursos em outros serviços (BigQuery, Storage, etc.), inclua os papéis correspondentes. Caso esteja em dúvida, usar um projeto onde você é Owner simplifica o início.

- Instalação e verificação do UV
  - Após instalar: `uv --version` deve mostrar a versão. Se o comando não aparecer, reinicie o terminal ou rode `source $HOME/.local/bin/env` novamente.
  - Python no Cloud Shell geralmente já está disponível; o `uv` criará e gerenciará o ambiente virtual automaticamente.

- Comandos gcloud úteis
  - Definir projeto: `gcloud config set project <ID_DO_PROJETO>` (já está no guia)
  - Validar conta e ADC: `gcloud auth list` e `gcloud auth application-default print-access-token` (para confirmar que a autenticação está funcionando)
  - Habilitar API Vertex AI: `make gcloud_ai_enable` (atalho via Makefile)
  - Fazer login ADC: `make gcloud_login` (atalho via Makefile)

- Abrir o editor do Cloud Shell
  - A instrução `cloudshell open-workspace .` pode variar. Alternativas:
    - Use o botão do Editor (ícone de lápis) no topo do Cloud Shell.
    - Ou `cloudshell open --` (em alguns ambientes) para abrir o diretório atual.

- Preparar o ambiente com Makefile (atalhos)
  - Criar venv: `make venv`
  - Sincronizar dependências: `make sync`
  - Ativar venv (opcional, para shells interativos): `make source` (equivalente a `source .venv/bin/activate`)

- Variáveis de ambiente (.env)
  - Existem arquivos `.env.template` nos diretórios
  - Copie o template para `.env` no respectivo diretório e preencha as chaves necessárias (APIs externas, projeto/região, etc.).
  - Certifique-se de que o projeto/região do Vertex AI estejam corretos, e que a autenticação ADC esteja ativa (passo do gcloud).

- Como executar os demos (servidores ADK e MCP)
  - ADK Web (UI para agentes em `src/agents`):
    - `make adk`  (inicia em http://localhost:8080 no Cloud Shell; use Web Preview para abrir a porta 8080)
  - ADK API (somente API):
    - `make adk_api`
  - Dica: use apenas um serviço por porta. Se necessário, altere a porta com a flag `--port` nos comandos do Makefile.

- Troubleshooting rápido
  - `uv: command not found`: rode `source $HOME/.local/bin/env` ou reinicie o terminal.
  - Permissão negada ao chamar Vertex AI: verifique `gcloud config get-value project`, os papéis IAM, e se as APIs 
    `aiplatform.googleapis.com` e `geminidataanalytics.googleapis.com` estão habilitadas.
  - Variáveis ausentes: confira se o arquivo `.env` foi criado a partir do `.env.template` correto.
  - Porta em uso: mude a porta (ex.: `uv run adk web src/agents --port 8081`) ou finalize o processo anterior.

- Limpeza e encerramento
  - Para parar um servidor, use Ctrl+C no terminal onde ele está rodando.
  - Para sair do ambiente virtual: `deactivate` (se você o ativou manualmente).

