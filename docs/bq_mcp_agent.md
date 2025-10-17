# BQ MCP Agent

## Visão Geral

O **BQ MCP Agent** é um agente especializado em análise de dados do BigQuery utilizando o **MCP (Model Context Protocol)** para gerenciamento centralizado de ferramentas. Este agente demonstra uma arquitetura moderna onde as ferramentas de acesso a dados são desacopladas do agente, permitindo maior flexibilidade, reutilização e manutenção.

## Características

- **Modelo**: Gemini 2.0 Flash
- **Protocolo**: MCP (Model Context Protocol)
- **Arquitetura**: Desacoplada e centralizada
- **Gerenciamento**: Ferramentas centralizadas via MCP Toolbox
- **Autenticação**: Gerenciada pelo servidor MCP

## O que é MCP (Model Context Protocol)?

O **Model Context Protocol (MCP)** é um protocolo padronizado que permite a comunicação entre modelos de linguagem (LLMs) e ferramentas externas de forma desacoplada e centralizada. Com MCP:

- **Centralização**: Um único servidor MCP gerencia autenticação e acesso a ferramentas
- **Desacoplamento**: Agentes não precisam conhecer detalhes de implementação das ferramentas
- **Reutilização**: Múltiplos agentes podem usar as mesmas ferramentas via MCP
- **Padronização**: Interface consistente para diferentes tipos de ferramentas
- **Manutenção**: Atualizações de ferramentas não requerem mudanças nos agentes

### Diferença entre BQ Tool Agent e BQ MCP Agent

| Aspecto | BQ Tool Agent | BQ MCP Agent |
|---------|---------------|--------------|
| **Ferramentas** | ADK BigQuery Toolset (nativo) | MCP Toolset (protocolo) |
| **Autenticação** | Application Default Credentials (direto) | Gerenciada pelo servidor MCP |
| **Acoplamento** | Ferramentas integradas no agente | Ferramentas desacopladas via MCP |
| **Configuração** | Configuração no código do agente | Configuração no servidor MCP |
| **Reutilização** | Cada agente configura suas ferramentas | Ferramentas compartilhadas entre agentes |
| **Manutenção** | Mudanças requerem alteração do agente | Mudanças isoladas no servidor MCP |

## Arquitetura

```
┌─────────────────┐
│   BQ MCP Agent  │
│  (Gemini 2.0)   │
└────────┬────────┘
         │
         │ MCP Protocol
         ▼
┌─────────────────┐
│   MCP Server    │
│  (Centralized)  │
└────────┬────────┘
         │
         ├─► BigQuery API
         ├─► Cloud Storage
         └─► Outras ferramentas...
```

## Configuração

### Pré-requisitos

1. **Google Cloud SDK** instalado e configurado
2. **Servidor MCP** configurado e em execução
3. **Permissões necessárias** no BigQuery:
   - `bigquery.datasets.get`
   - `bigquery.tables.get`
   - `bigquery.tables.list`
   - `bigquery.jobs.create`

### Configurando o Servidor MCP

O servidor MCP precisa ser configurado para fornecer acesso ao BigQuery. Existem diferentes formas de configurar:

#### Opção 1: Configuração via Arquivo

Crie um arquivo de configuração MCP (exemplo: `mcp_config.json`):

```json
{
  "mcpServers": {
    "bigquery": {
      "command": "mcp-server-bigquery",
      "args": [],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account.json",
        "GOOGLE_CLOUD_PROJECT": "your-project-id"
      }
    }
  }
}
```

#### Opção 2: FastMCP Server

Use o FastMCP para criar um servidor MCP customizado:

```python
# mcp_server.py
from fastmcp import FastMCP
from google.cloud import bigquery

mcp = FastMCP("BigQuery MCP Server")

@mcp.tool()
async def execute_query(query: str, project_id: str) -> dict:
    """Execute a BigQuery SQL query"""
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    results = query_job.result()

    return {
        "rows": [dict(row) for row in results],
        "total_rows": results.total_rows
    }

@mcp.tool()
async def list_datasets(project_id: str) -> list:
    """List all datasets in a project"""
    client = bigquery.Client(project=project_id)
    datasets = list(client.list_datasets())

    return [dataset.dataset_id for dataset in datasets]

if __name__ == "__main__":
    mcp.run()
```

Execute o servidor:

```bash
# Instale o FastMCP
uv pip install fastmcp

# Execute o servidor
python mcp_server.py
```

#### Opção 3: MCP Server BigQuery Oficial

Se disponível, use o servidor MCP oficial do BigQuery:

```bash
# Instale o servidor MCP do BigQuery
npm install -g @modelcontextprotocol/server-bigquery

# Configure as credenciais
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"

# Execute o servidor
mcp-server-bigquery
```

## Como Usar

### Execução Básica

```bash
# 1. Certifique-se que o servidor MCP está em execução
# (veja seção de configuração acima)

# 2. Execute o agente
uv run adk web src/agents
```

### Autenticação

```bash
# Configure Application Default Credentials
gcloud auth application-default login --no-launch-browser

# Ou use Service Account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Exemplos de Uso

#### 1. Consulta Básica

```
User: Quantas tabelas existem no dataset 'my_dataset' no projeto 'my-project'?
Agent: [Usa MCP tools para consultar o BigQuery]
```

#### 2. Análise de Dados

```
User: Analise as vendas do último trimestre no dataset analytics

Agent: Vou analisar os dados de vendas para você.
[Executa queries via MCP]

Resultados encontrados:
- Total de vendas: R$ 1.2M
- Crescimento: +15% vs Q anterior
- Principais produtos: [lista]
```

#### 3. Exploração de Datasets Públicos

```
User: Explore o dataset de táxis de Nova York e me dê insights sobre gorjetas

Agent: [Usa MCP para acessar bigquery-public-data.new_york_taxi_trips]
```

## Fluxo de Trabalho Recomendado

### 1. Compreensão da Solicitação

- Analise cuidadosamente o que o usuário precisa
- Identifique quais dados são necessários
- Planeje a abordagem de análise

### 2. Consulta de Dados

- Use as ferramentas MCP para acessar o BigQuery
- Construa queries SQL eficientes e bem estruturadas
- Valide resultados antes de apresentar

### 3. Análise e Insights

- Interprete os dados obtidos
- Identifique padrões e tendências
- Forneça insights acionáveis

### 4. Apresentação

- Formate resultados de forma clara
- Explique o significado dos dados
- Sugira próximos passos ou análises complementares

## Vantagens do MCP

### 1. Gerenciamento Centralizado

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Agent A     │────►│              │     │              │
│  (BQ MCP)    │     │              │     │              │
└──────────────┘     │  MCP Server  │────►│  BigQuery    │
┌──────────────┐     │  (Central)   │     │              │
│  Agent B     │────►│              │     │              │
│  (Analytics) │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

Múltiplos agentes acessam as mesmas ferramentas sem duplicação de código.

### 2. Autenticação Simplificada

- Credenciais gerenciadas centralmente no servidor MCP
- Agentes não precisam conhecer detalhes de autenticação
- Facilita rotação de credenciais

### 3. Suporte Multi-Ferramenta

```python
# Um agente pode acessar múltiplas ferramentas via MCP
bq_mcp_agent = LlmAgent(
    model=MODEL,
    name="multi_tool_agent",
    tools=[mcp_toolset]  # Pode incluir BigQuery, Storage, etc.
)
```

### 4. Desacoplamento

- Atualizações de ferramentas não afetam agentes
- Fácil adicionar novas ferramentas
- Agentes focam em lógica de negócio

## Comparação com BQ Tool Agent

### Quando usar BQ Tool Agent?

- **Simplicidade**: Para projetos simples ou prototipagem rápida
- **Controle direto**: Quando você precisa de controle fino sobre as ferramentas
- **Self-contained**: Aplicações que precisam ser independentes
- **Performance**: Quando latência mínima é crítica (sem hop extra do MCP)

### Quando usar BQ MCP Agent?

- **Múltiplos agentes**: Vários agentes precisam das mesmas ferramentas
- **Centralização**: Gerenciamento centralizado de credenciais e políticas
- **Escalabilidade**: Arquitetura que precisa escalar com novos agentes
- **Manutenção**: Facilitar atualizações sem modificar agentes
- **Multi-tenant**: Diferentes equipes usando ferramentas compartilhadas

## Exemplos Práticos

### Exemplo 1: Query Simples

```
User: Quantos registros tem a tabela users no dataset analytics?

Agent: Vou consultar essa informação para você.

[Via MCP] Executando query:
SELECT COUNT(*) as total
FROM `my-project.analytics.users`

Resultado: A tabela users contém 45,289 registros.
```

### Exemplo 2: Análise Complexa

```
User: Analise o comportamento de compra dos usuários em 2024

Agent: Vou realizar uma análise completa do comportamento de compra.

[Via MCP] Etapas:
1. Identificando datasets relevantes...
2. Explorando schemas de tabelas...
3. Construindo queries de análise...
4. Agregando resultados...

Insights encontrados:
- Ticket médio: R$ 350
- Frequência média: 2.3 compras/mês
- Taxa de recompra: 67%
- Horários de pico: 19h-21h
- Categorias mais vendidas: [lista]

Recomendações:
- Focar em campanhas para horário de pico
- Programa de fidelidade pode aumentar recompra
```

### Exemplo 3: Dados Públicos

```
User: Compare os padrões de táxi em NY entre dias úteis e fins de semana

Agent: Vou analisar os dados de táxi de Nova York.

[Via MCP] Acessando bigquery-public-data.new_york_taxi_trips...

Comparação Dias Úteis vs Fins de Semana:

Dias Úteis:
- Volume: 450k corridas/dia
- Horário pico: 8h-9h e 17h-19h
- Gorjeta média: 18.5%
- Distância média: 3.2 milhas

Fins de Semana:
- Volume: 320k corridas/dia
- Horário pico: 22h-2h
- Gorjeta média: 21.3%
- Distância média: 4.7 milhas

Insights:
- Fins de semana têm corridas mais longas (+47%)
- Gorjetas maiores à noite (+15%)
- Volume reduzido mas mais lucrativo por corrida
```

## Troubleshooting

### Erro: "MCP server not found"

```bash
# Verifique se o servidor MCP está rodando
ps aux | grep mcp

# Ou verifique a configuração MCP
cat mcp_config.json
```

### Erro: "Authentication failed"

```bash
# Configure ADC
gcloud auth application-default login --no-launch-browser

# Ou verifique service account
echo $GOOGLE_APPLICATION_CREDENTIALS
cat $GOOGLE_APPLICATION_CREDENTIALS
```

### Erro: "Connection refused"

```bash
# Verifique se o servidor MCP está acessível
# Se usando porta padrão MCP (geralmente 8000)
curl http://localhost:8000/health

# Verifique logs do servidor MCP
tail -f /var/log/mcp/server.log
```

### Erro: "Tool not found"

O servidor MCP pode não estar expondo as ferramentas necessárias:

```bash
# Liste ferramentas disponíveis no MCP
mcp list-tools

# Ou adicione ferramentas ao servidor MCP
# Edite sua configuração do servidor
```

## Desenvolvimento e Extensão

### Adicionar Novas Ferramentas ao MCP Server

```python
# Exemplo: Adicionar ferramenta de análise customizada
from fastmcp import FastMCP

mcp = FastMCP("Enhanced BigQuery MCP")

@mcp.tool()
async def custom_analysis(dataset: str, metric: str) -> dict:
    """Perform custom analysis on dataset"""
    # Sua lógica customizada
    client = bigquery.Client()

    # Exemplo: análise de tendências
    query = f"""
    SELECT
        DATE_TRUNC(date, MONTH) as month,
        AVG({metric}) as avg_value
    FROM `{dataset}`
    GROUP BY month
    ORDER BY month
    """

    results = client.query(query).result()
    return {"trends": [dict(row) for row in results]}

# Adicionar ao servidor
mcp.run()
```

### Teste de Ferramentas MCP

```bash
# Use o CLI do FastMCP para testar
fastmcp dev mcp_server.py

# Ou teste individualmente
python -c "
from mcp_server import execute_query
result = execute_query('SELECT 1', 'my-project')
print(result)
"
```

## Monitoramento

### Logs do MCP Server

```bash
# Configure logging no servidor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)
```

### Métricas

```python
# Adicione métricas ao servidor MCP
from prometheus_client import Counter, Histogram

query_counter = Counter('mcp_queries_total', 'Total queries executed')
query_duration = Histogram('mcp_query_duration_seconds', 'Query duration')

@mcp.tool()
async def execute_query_with_metrics(query: str) -> dict:
    query_counter.inc()
    with query_duration.time():
        # Execute query
        result = execute_query(query)
    return result
```

## Recursos Adicionais

### Documentação

- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **FastMCP**: https://github.com/jlowin/fastmcp
- **Google ADK MCP Tools**: https://github.com/google/adk
- **BigQuery Documentation**: https://cloud.google.com/bigquery/docs

### Servidores MCP Populares

- **@modelcontextprotocol/server-bigquery**: Servidor oficial BigQuery
- **@modelcontextprotocol/server-postgres**: Servidor PostgreSQL
- **@modelcontextprotocol/server-filesystem**: Acesso a arquivos
- **FastMCP**: Framework Python para criar servidores customizados

### Datasets Públicos

Para exemplos práticos, use os mesmos datasets públicos listados na [documentação do BQ Tool Agent](./bq_tool_agent.md#5-datasets-públicos-do-bigquery).

## Localização do Código

- **Agent**: `src/agents/bq_mcp/agent.py`
- **Prompt**: `src/agents/bq_mcp/prompt.py`
- **Init**: `src/agents/bq_mcp/__init__.py`

## Próximos Passos

1. **Configure seu servidor MCP**: Escolha entre FastMCP ou servidor oficial
2. **Teste com datasets públicos**: Use `bigquery-public-data` para validar
3. **Implemente ferramentas customizadas**: Estenda o servidor MCP conforme necessário
4. **Monitore performance**: Adicione logging e métricas
5. **Escale horizontalmente**: Adicione mais servidores MCP conforme demanda

## Comparação Final: BQ Tool vs BQ MCP

```
BQ Tool Agent                    BQ MCP Agent
     │                                │
     ├─ Ferramentas ADK              ├─ MCP Toolset
     │  (integradas)                 │  (desacopladas)
     │                               │
     ├─ Auth direto (ADC)            ├─ Auth via MCP Server
     │                               │
     ├─ Simples e direto             ├─ Arquitetura escalável
     │                               │
     └─ Melhor para single-agent     └─ Melhor para multi-agent
```

Escolha baseado nas necessidades do seu projeto!
