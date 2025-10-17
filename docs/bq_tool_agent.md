# BQ Tool Agent

## Visão Geral

O **BQ Tool Agent** é um agente especializado em análise de dados do BigQuery utilizando ferramentas nativas do Google ADK (Agent Development Kit). Este agente permite explorar datasets, consultar schemas de tabelas e executar queries SQL diretamente no BigQuery através de uma interface conversacional.

## Características

- **Modelo**: Gemini 2.0 Flash
- **Modo de Escrita**: BLOCKED (somente leitura)
- **Autenticação**: Application Default Credentials (ADC)
- **Ferramentas**: BigQuery Toolset nativo do ADK

## Ferramentas Disponíveis

O agente tem acesso às seguintes ferramentas do BigQuery:

1. **list_dataset_ids**: Lista todos os datasets disponíveis no projeto
2. **get_dataset_info**: Obtém informações detalhadas sobre um dataset específico
3. **list_table_ids**: Lista todas as tabelas dentro de um dataset
4. **get_table_info**: Obtém schema e metadados de uma tabela específica
5. **execute_sql**: Executa queries SQL no BigQuery

## Configuração

### Pré-requisitos

1. **Google Cloud SDK** instalado e configurado
2. **Application Default Credentials (ADC)** configuradas
3. **Permissões necessárias** no BigQuery:
   - `bigquery.datasets.get`
   - `bigquery.tables.get`
   - `bigquery.tables.list`
   - `bigquery.jobs.create`

### Configurando Credenciais

Configure suas credenciais usando um dos métodos abaixo:

```bash
# Login com sua conta Google
gcloud auth application-default login --no-launch-browser
```
## Como Usar

### Execução Básica

```bash
# Execute o agente
uv run adk web src/agents
```

### Exemplos de Uso

#### 1. Explorar Datasets Disponíveis

```
User: Quais datasets estão disponíveis no projeto?
Agent: [Lista todos os datasets usando list_dataset_ids]
```

#### 2. Explorar Estrutura de Tabelas

```
User: Quais tabelas existem no dataset 'my_dataset'?
Agent: [Lista tabelas usando list_table_ids]

User: Me mostre o schema da tabela 'users'
Agent: [Mostra schema detalhado usando get_table_info]
```

#### 3. Executar Queries SQL

```
User: Quantos usuários estão cadastrados?
Agent: [Executa query usando execute_sql]
SELECT COUNT(*) as total_users FROM `project.dataset.users`
```

#### 4. Análise de Dados

```
User: Me mostre os 10 produtos mais vendidos no último mês
Agent: [Explora schema, constrói e executa query apropriada]
```

#### 5. Datasets Públicos do BigQuery

O Google Cloud oferece diversos datasets públicos gratuitos no projeto `bigquery-public-data` que você pode usar para testar e explorar o agente. Aqui estão alguns dos mais populares:

##### Datasets de Negócios e E-commerce

**1. Google Analytics Sample**
- **Dataset**: `bigquery-public-data.ga4_obfuscated_sample_ecommerce`
- **Descrição**: Dados de amostra do Google Analytics 4 de um e-commerce
- **Tabelas principais**: `events_*` (eventos diários)
- **Uso**: Análise de comportamento de usuários, funis de conversão, análise de produtos

```sql
-- Exemplo: Top 10 páginas mais visitadas
SELECT
  (SELECT value.string_value FROM UNNEST(event_params)
   WHERE key = 'page_location') as page,
  COUNT(*) as page_views
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name = 'page_view'
GROUP BY page
ORDER BY page_views DESC
LIMIT 10
```

**2. Iowa Liquor Sales**
- **Dataset**: `bigquery-public-data.iowa_liquor_sales`
- **Tabela**: `sales`
- **Descrição**: Vendas de bebidas alcoólicas em Iowa (2012-presente)
- **Uso**: Análise de vendas, previsão de demanda, análise geográfica

```sql
-- Exemplo: Vendas por categoria de produto
SELECT
  category_name,
  COUNT(*) as num_sales,
  ROUND(SUM(sale_dollars), 2) as total_revenue
FROM `bigquery-public-data.iowa_liquor_sales.sales`
WHERE DATE(date) >= '2024-01-01'
GROUP BY category_name
ORDER BY total_revenue DESC
LIMIT 10
```

##### Datasets de Dados Abertos e Governamentais

**3. New York Taxi Trips**
- **Dataset**: `bigquery-public-data.new_york_taxi_trips`
- **Tabelas**: `tlc_yellow_trips_*`, `tlc_green_trips_*`
- **Descrição**: Dados de corridas de táxi em Nova York
- **Uso**: Análise de mobilidade urbana, padrões de viagem, análise temporal

```sql
-- Exemplo: Média de gorjetas por hora do dia
SELECT
  EXTRACT(HOUR FROM pickup_datetime) as hour,
  AVG(tip_amount) as avg_tip,
  COUNT(*) as num_trips
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2024`
WHERE tip_amount > 0
GROUP BY hour
ORDER BY hour
```

**4. COVID-19 Data**
- **Dataset**: `bigquery-public-data.covid19_open_data`
- **Tabela**: `covid19_open_data`
- **Descrição**: Dados globais sobre COVID-19
- **Uso**: Análise epidemiológica, tendências por região

```sql
-- Exemplo: Casos por país nos últimos 30 dias
SELECT
  country_name,
  SUM(new_confirmed) as total_new_cases,
  SUM(new_deceased) as total_deaths
FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND country_name IS NOT NULL
GROUP BY country_name
ORDER BY total_new_cases DESC
LIMIT 20
```

##### Datasets de Tecnologia e Web

**5. GitHub Repositories**
- **Dataset**: `bigquery-public-data.github_repos`
- **Tabelas**: `commits`, `files`, `languages`, `licenses`
- **Descrição**: Dados de repositórios públicos do GitHub
- **Uso**: Análise de código open source, tendências de linguagens

```sql
-- Exemplo: Linguagens de programação mais populares
SELECT
  language.name,
  COUNT(DISTINCT repo_name) as num_repos,
  SUM(language.bytes) as total_bytes
FROM `bigquery-public-data.github_repos.languages`,
  UNNEST(language) as language
GROUP BY language.name
ORDER BY num_repos DESC
LIMIT 15
```

**6. Stack Overflow**
- **Dataset**: `bigquery-public-data.stackoverflow`
- **Tabelas**: `posts_questions`, `posts_answers`, `users`, `tags`
- **Descrição**: Dados do Stack Overflow
- **Uso**: Análise de tendências tecnológicas, análise de comunidade

```sql
-- Exemplo: Tags mais populares do ano
SELECT
  tag,
  COUNT(*) as question_count
FROM `bigquery-public-data.stackoverflow.posts_questions`,
  UNNEST(SPLIT(tags, '|')) as tag
WHERE EXTRACT(YEAR FROM creation_date) = 2024
GROUP BY tag
ORDER BY question_count DESC
LIMIT 20
```

##### Datasets de Clima e Ambiente

**7. NOAA Weather Data**
- **Dataset**: `bigquery-public-data.noaa_gsod`
- **Tabelas**: `gsod*` (por ano)
- **Descrição**: Dados meteorológicos globais
- **Uso**: Análise climática, previsões, tendências

```sql
-- Exemplo: Temperaturas médias por estação em 2024
SELECT
  stn,
  name,
  AVG(temp) as avg_temp,
  COUNT(*) as measurements
FROM `bigquery-public-data.noaa_gsod.gsod2024`
WHERE temp IS NOT NULL AND temp < 200
GROUP BY stn, name
ORDER BY avg_temp DESC
LIMIT 10
```

##### Datasets Financeiros

**8. Bitcoin Blockchain**
- **Dataset**: `bigquery-public-data.crypto_bitcoin`
- **Tabelas**: `transactions`, `blocks`
- **Descrição**: Dados da blockchain do Bitcoin
- **Uso**: Análise de transações, volume de negociações

```sql
-- Exemplo: Volume de transações por dia
SELECT
  DATE(block_timestamp) as date,
  COUNT(*) as num_transactions,
  SUM(output_value) as total_value
FROM `bigquery-public-data.crypto_bitcoin.transactions`
WHERE DATE(block_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date DESC
```

##### Datasets de Entretenimento

**9. IMDb Movies**
- **Dataset**: `bigquery-public-data.imdb`
- **Tabelas**: `title_basics`, `title_ratings`, `name_basics`
- **Descrição**: Dados de filmes e séries do IMDb
- **Uso**: Análise de tendências em entretenimento

```sql
-- Exemplo: Filmes mais bem avaliados de 2024
SELECT
  tb.primary_title,
  tb.start_year,
  tr.average_rating,
  tr.num_votes
FROM `bigquery-public-data.imdb.title_basics` tb
JOIN `bigquery-public-data.imdb.title_ratings` tr
  ON tb.tconst = tr.tconst
WHERE tb.title_type = 'movie'
  AND tb.start_year = 2024
  AND tr.num_votes > 1000
ORDER BY tr.average_rating DESC
LIMIT 20
```

##### Como Usar com o BQ Tool Agent

Para explorar esses datasets com o agente:

```
User: Liste as tabelas disponíveis no dataset bigquery-public-data.iowa_liquor_sales

User: Me mostre o schema da tabela sales

User: Quais foram os produtos mais vendidos em 2024?

User: Analise as tendências de vendas por mês no último ano
```

##### Recursos Adicionais

- **Catálogo completo**: https://cloud.google.com/bigquery/public-data
- **Marketplace**: https://console.cloud.google.com/marketplace/browse?filter=solution-type:dataset
- **Documentação**: https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console

**Nota**: Consultas em datasets públicos são gratuitas até 1 TB por mês. Custos de processamento se aplicam após esse limite.

## Fluxo de Trabalho Recomendado

### 1. Exploração

O agente sempre seguirá estas práticas:

- Listar datasets disponíveis se não souber onde os dados estão
- Explorar a estrutura das tabelas antes de fazer queries
- Verificar schemas para entender os tipos de dados

### 2. Análise

- Construir queries SQL apropriadas baseadas na solicitação
- Usar boas práticas de SQL (LIMIT para testes, otimização)
- Considerar custos de processamento

### 3. Apresentação

- Formatar resultados de forma clara e legível
- Explicar insights encontrados nos dados
- Sugerir análises complementares quando apropriado

## Diretrizes de Segurança

### Modo de Escrita

O agente está configurado com `WriteMode.BLOCKED`, o que significa:

- **Somente leitura**: Não pode criar, modificar ou deletar dados
- **Queries seguras**: Apenas operações SELECT são permitidas
- **Proteção de dados**: Previne modificações acidentais

### Modos Disponíveis

```python
# BLOCKED - Somente leitura (padrão)
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

# PROTECTED - Permite escrita apenas em dados temporários
tool_config = BigQueryToolConfig(write_mode=WriteMode.PROTECTED)

# ALLOWED - Permite escrita completa (use com cuidado!)
tool_config = BigQueryToolConfig(write_mode=WriteMode.ALLOWED)
```

## Referências

- [Google ADK Documentation](https://github.com/google/adk)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc)

## Localização do Código

- **Agent**: `src/agents/bq_tool/agent.py`
- **Prompt**: `src/agents/bq_tool/prompt.py`
- **Init**: `src/agents/bq_tool/__init__.py`