# Decisões Técnicas

Esse documento registra as principais decisões técnicas tomadas durante o desenvolvimento do projeto **Cloud-Native Credit Risk Data Pipeline**. A ideia é manter um histórico claro das escolhas feitas, os motivos e possíveis evoluções futuras.

---

## 1. Evoluir o projeto original para uma V2 cloud-native

### Decisão

Criar uma segunda versão do projeto `credit-risk-data-pipeline`, agora utilizando serviços da Google Cloud.

### Motivo

A primeira versão trazia um pipeline local com Python, Parquet e SQL Server. Então a V2 foi criada para ampliar a complexidade técnica e aproximar o projeto de um cenário real de engenharia de dados.

### Resultado

A V2 passou a incluir:

- Google Cloud Storage
- BigQuery
- Views analíticas
- Looker Studio
- Arquitetura Medallion em ambiente cloud

> [!IMPORTANT]
> Essa decisão consiste em uma evolução técnica do projeto, não apenas a repetição de uma solução já feita.

---

## 2. Utilizar Arquitetura Medallion

### Decisão

Separar o fluxo do dado em três camadas:

```text
Bronze → Silver → Gold
```

### Motivo

Essa arquitetura melhora:

- Organização do pipeline
- Rastreabilidade dos dados
- Clareza entre dado bruto, tratado e analítico
- Manutenção futura
- Escalabilidade do projeto

### Aplicação no projeto

| Camada | Conteúdo |
|---|---|
| Bronze | Dataset original baixado da UCI |
| Silver | Dados tratados e padronizados |
| Gold | Agregações para análise |

---

## 3. Manter os arquivos locais fora do GitHub

### Decisão

Não versionar os arquivos gerados em `data/`.

### Motivo

Os dados podem ser reproduzidos pelo pipeline. Então não faz sentido armazenar arquivos gerados no repositório, especialmente se futuramente o volume aumentar.

### Itens ignorados

```text
data/
*.parquet
*.data
```

> [!TIP]
> O código cria automaticamente as pastas `data/bronze`, `data/silver` e `data/gold` durante a execução.

---

## 4. Usar Parquet nas camadas Silver e Gold

### Decisão

Salvar os arquivos tratados e analíticos em formato `.parquet`.

### Motivo

Parquet é um formato colunar amplamente usado em engenharia de dados por oferecer:

- Melhor compressão
- Melhor performance analítica
- Compatibilidade com BigQuery
- Organização eficiente de dados tabulares

### Arquivos gerados

```text
german_credit_silver.parquet
credit_risk_summary.parquet
purpose_risk_summary.parquet
age_risk_summary.parquet
```

---

## 5. Usar Google Cloud Storage como Data Lake

### Decisão

Enviar os arquivos Bronze, Silver e Gold para um bucket no Google Cloud Storage.

### Motivo

O GCS permite simular uma camada de Data Lake em nuvem.

### Estrutura usada

```text
bronze/
silver/
gold/
```

### Resultado

Os dados ficam disponíveis em ambiente cloud e podem ser consumidos por outros serviços.

---

## 6. Usar BigQuery como Data Warehouse

### Decisão

Carregar as tabelas Silver e Gold no BigQuery.

### Motivo

O BigQuery é um serviço gerenciado, escalável e integrado ao ecossistema Google Cloud.

Ele permite:

- Consultas SQL
- Integração com Looker Studio
- Criação de views
- Análises rápidas
- Separação entre armazenamento bruto e camada analítica

---

## 7. Criar views para consumo analítico

### Decisão

Criar views no BigQuery para facilitar o uso dos dados no dashboard.

### Motivo

O dashboard não deve carregar toda a responsabilidade de tratamento e tradução dos dados.

As views ajudam a:

- Traduzir campos técnicos
- Padronizar nomes de colunas
- Facilitar análise
- Reduzir retrabalho no Looker Studio

### Exemplo

```sql
CASE target_label
    WHEN 'good' THEN 'Bom'
    WHEN 'bad' THEN 'Mau'
    ELSE target_label
END AS perfil_cliente
```

---

## 8. Tornar a view de finalidade robusta

### Decisão

A view `vw_purpose_risk_summary` considera tanto os códigos originais (`A40`, `A41`) quanto os valores tratados (`car_new`, `car_used`), mas não atoa.

### Motivo

Durante o desenvolvimento, o BigQuery chegou a conter dados com códigos originais. Ao rodar o pipeline do zero, o mapeamento pode transformar esses códigos em nomes técnicos em inglês.

Para evitar inconsistência, a view foi criada para lidar com os dois cenários.

### Exemplo

```sql
CASE purpose
    WHEN 'A40' THEN 'Carro novo'
    WHEN 'car_new' THEN 'Carro novo'
    WHEN 'A41' THEN 'Carro usado'
    WHEN 'car_used' THEN 'Carro usado'
    ELSE purpose
END AS finalidade_credito
```

> [!NOTE]
> Essa decisão evita que o dashboard quebre caso o dado venha em uma das duas representações por algum motivo.

---

## 9. Criar views manualmente no BigQuery

### Decisão

Manter a criação das views de forma manual pelo arquivo:

```text
sql/create_bigquery_views.sql
```

### Motivo

A decisão foi tomada para reforçar o aprendizado prático no BigQuery e manter controle explícito sobre a camada analítica.

### Limitação

O `main.py` não recria as views automaticamente.

### Evolução futura

Automatizar a criação das views via:

- Python
- dbt
- Terraform
- GitHub Actions

> [!WARNING]
> Após rodar o pipeline, se as tabelas forem recriadas, pode ser necessário executar novamente o script de views no BigQuery (por isso nas views são considerados tanto os códigos originais (`A40`, `A41`) quanto os valores tratados, pra evitar inconsistencias).

---

## 10. Usar `.env` para configurações

### Decisão

Centralizar configurações em variáveis de ambiente.

### Motivo

Evita deixar informações específicas do ambiente diretamente no código.

### Variáveis usadas

```env
PROJECT_ID=
BUCKET_NAME=
DATASET_ID=
REGION=
GOOGLE_APPLICATION_CREDENTIALS=
```

---

## 11. Não versionar credenciais

### Decisão

Adicionar `.env`, `credentials/` e arquivos `.json` ao `.gitignore`.

### Motivo

Arquivos JSON de Service Account contêm chaves privadas e nunca devem ser enviados para repositórios públicos.

### Itens protegidos

```text
.env
credentials/
*.json
```

> [!IMPORTANT]
> O nome do projeto, bucket e dataset deixei aparecer na documentação pois não são sensíveis e ajudam no entendimento do projeto. O que não pode aparecer são chaves, tokens, senhas e arquivos de credenciais.

---

## 12. Usar Looker Studio para visualização

### Decisão

Criar um dashboard no Looker Studio a partir das views do BigQuery.

### Motivo

A visualização ajuda a validar se a camada analítica está útil para consumo final.

### Métricas exibidas

- Total de clientes
- Ticket médio
- Bons pagadores
- Maus pagadores
- Distribuição por faixa etária
- Distribuição por finalidade de crédito

---

## 13. Manter o pipeline simples na V2

### Decisão

Não incluir, nesta versão inicial:

- Terraform
- Airflow
- Docker
- dbt
- CI/CD
- Testes automatizados

### Motivo

O foco desta V2 foi validar o fluxo cloud-native completo de ponta a ponta.

> [!TIP]
> Pois eu acredito que é melhor entregar uma V2 funcional e bem documentada do que criar uma arquitetura gigante que não fecha o ciclo completo.

---

## Resumo das Decisões

| Decisão | Status |
|---|---|
| Evoluir projeto para cloud | Implementado |
| Usar Medallion Architecture | Implementado |
| Usar Parquet | Implementado |
| Usar GCS | Implementado |
| Usar BigQuery | Implementado |
| Criar views analíticas | Implementado |
| Criar dashboard no Looker Studio | Implementado |
| Automatizar views | Futuro |
| Adicionar testes | Futuro |
| Provisionar infra com Terraform | Futuro |