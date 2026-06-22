# ☁️Cloud-Native Credit Risk Data Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-GCP-orange)
![BigQuery](https://img.shields.io/badge/BigQuery-Data%20Warehouse-blue)
![Cloud Storage](https://img.shields.io/badge/Cloud%20Storage-Object%20Storage-green)
![Looker Studio](https://img.shields.io/badge/Looker-DataStudio-darkblue)
![Architecture](https://img.shields.io/badge/Architecture-Medallion-purple)

Pipeline de dados cloud-native end-to-end para análise de risco de crédito utilizando **Python**, **Google Cloud Storage**, **BigQuery** e **Looker Studio**, seguindo a arquitetura **Medallion (Bronze → Silver → Gold)**.

> [!IMPORTANT]
> Esse projeto é uma evolução cloud-native do projeto **credit-risk-data-pipeline**.
>
> Enquanto a V1 utilizava processamento local com SQL Server, essa V2 expande a arquitetura para a nuvem utilizando serviços gerenciados da Google Cloud Platform (GCP).
>
> 🔗 Repositório da V1: https://github.com/M1llyz/credit-risk-data-pipeline

---

## 📖 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dashboard Analítico](#dashboard-analítico)
- [Resultados e Insights](#resultados-e-insights)
- [Como Executar](#como-executar)
- [Configuração da Google Cloud](#configuração-da-google-cloud)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Fluxo do Pipeline](#fluxo-do-pipeline)
- [Camadas Medallion](#camadas-medallion)
- [BigQuery e Views Analíticas](#bigquery-e-views-analíticas)
- [Roadmap](#roadmap)

---

## ℹ️ Sobre o Projeto

O objetivo do projeto é demonstrar a construção de um pipeline moderno de engenharia de dados para análise de risco de crédito mas agora utilizando recursos da Google Cloud Platform.

O pipeline realiza:

- Download automático do dataset German Credit Dataset (UCI)
- Processamento e padronização dos dados
- Aplicação da arquitetura Medallion
- Armazenamento em Cloud Storage
- Carregamento para BigQuery
- Criação de views analíticas
- Consumo dos dados no Looker Studio

---

## 🏗️ Arquitetura

<p align="center">
<img src="assets\diagram_architecture_pipeline.png" width="100%" alt="Diagrama da Arquitetura do Pipeline" />
</p>

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

| Categoria | Ferramenta |
|------------|------------|
| Linguagem | Python |
| Processamento | Pandas |
| Armazenamento | Parquet |
| Cloud Storage | Google Cloud Storage |
| Data Warehouse | BigQuery |
| Visualização | Looker Studio |
| Versionamento | Git/GitHub |

---

## 📁 Estrutura do Projeto

```text
v2.cloud-credit-risk
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── cloud/
│   └── config/
│
├── sql/
│   ├── create_bigquery_views.sql
│   └── sample_questions.sql
│
├── docs/
│   ├── architecture.md
│   ├── gcp_setup.md
│   ├── decisions.md
│   ├── backlog.md
│   └── lessons_learned.md
│
├── credentials/
│
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📊 Dashboard Analítico

O projeto possui uma camada analítica consumida pelo Data Studio (antigo Looker Studio).

> [!NOTE]
>
>🔗 Dashboard público: https://datastudio.google.com/reporting/1bd69e6a-8541-4756-ae29-24eeb371ab9c

<p align="center">
<img src="assets\credit-risk-analytics-dashboard.png" width="100%" alt="Análise de Risco de Crédito — Dashboard" />
</p>

---

## 💡 Resultados e Insights

O objetivo do dashboard não é construir um modelo preditivo de crédito, mas disponibilizar uma camada analítica para exploração dos dados.

E nesse caso em especifico de um projeto para estudo, permite identificar se todo o fluxo foi devidamente concluído e está disponibilizando os dados corretos e tratados pra consumo (que me ajudou por exemplo a perceber que alguns dados não estavam chegando traduzidos pra criação do dash e com isso pude corrigir o que faltava).

Alguns insights observados:

| Insight | Observação |
|----------|------------|
| Perfil geral | 70% dos clientes foram classificados como bons pagadores |
| Faixa etária | Clientes entre 18 e 25 anos apresentaram maior proporção de maus pagadores |
| Finalidade mais frequente | Rádio/TV apresentou o maior volume de clientes |
| Ticket médio | Créditos para carro usado e negócios apresentaram valores médios mais elevados |
| Educação | Apesar do baixo volume, apresentou proporção relevante de maus pagadores |

---

## ▶️ Como Executar

### Pré-requisitos
Antes de executar o projeto, é necessário ter instalado/criado:

- Python 3.10+
- Git
- Conta Google Cloud Platform (GCP)
- Projeto criado na GCP
- Bucket no Cloud Storage
- Dataset no BigQuery
- Service Account com permissões adequadas

> [!TIP]
> Alguns desses eu ensino a criar/instalar mais abaixo e também nos arquivos da pasta docs com mais detalhes :)

---

### 1. Clonar o repositório

```bash
git clone https://github.com/M1llyz/v2.cloud-credit-risk.git
cd v2.cloud-credit-risk
```

---

## 2. Ativar ambiente virtual

```bash
python -m venv .venv
```

🪟 No Windows:

```bash
.venv\Scripts\activate
```

🐧 No Linux:

```bash
source .venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar credenciais

📂 Criar a pasta:

```text
credentials/
```

e colocar nela o arquivo JSON da Service Account (que explico como criar/gerar mais abaixo).

Exemplo:

```text
credentials/
└── project_id-service-account.json
```

> [!WARNING]
> Não compartilhe essas credenciais (adicione a pasta credentials no .gitignore caso vá subir um projeto usando a credential da GCP pro GitHub).

---

### 5. Configuração da Google Cloud

> [!IMPORTANT]
> Esse projeto utiliza serviços da Google Cloud Platform.
>
> Algumas operações podem gerar custos dependendo do volume processado e das configurações utilizadas na sua conta.
>
> Como o dataset que usei possui apenas 1.000 registros, os custos tendem a ser praticamente nulos durante os testes (usei 0,1 centavo e isso é tão pouco que entra dentro do limite do free tier da GCP e ela nem fatura isso)
>
> Mas caso se sinta mais seguro, você pode criar um alerta caso chegue a um determinado orçamento (por exemplo $1). Pra isso, acesse o menu --> Faturamento --> Orçamentos e Alertas e crie um pra que seja avisado por e-mail.

Após criar sua conta (a GCP oferece um free tier com um crédito bem legal pra novos usuários), siga o caminho abaixo

### ⚙️Recursos que são necessários criar:

### Projeto

```text
Em 'Novo Projeto' crie e nomeie seu projeto (algo como 'credit-risk-pipeline' por exemplo). Veja o ID do projeto que fica logo embaixo ao criar (coloque ele no .env)
```

### Bucket

```text
Depois de criar o projeto, precisamos criar um bucket, pra isso vamos usar o serviço Cloud Storage, crie e nomeie como preferir (mas lembre-se, esse nome precisa estar exatamente igual no .env)
```

### Dataset BigQuery

```text
Agora precisamos criar o dataset pra posteriormente usarmos pra consultas e consumir pra criação do dash. Pra isso, vamos usar o BigQuery, crie e nomeie o dataset (adicione o id do dataset no .env)
```

### APIs

```text
Habilite:

- BigQuery API
- Cloud Storage API
```

### Criar Service Account

> [!IMPORTANT]
>Pra fazer a conexão, precisamos de uma conta de serviço (fiz isso pra não precisar instalar o google cloud SDK / gcloud, mas fique a vontade pra seguir outra abordagem). Na GCP acesse o menu e siga: IAM & Admin → Service Accounts
>
>Crie uma nova conta de serviço.
>
>Com as permissões mínimas (papéis):
>
>- BigQuery Admin
>- Storage Admin
>
>Ao criar, gere a chave JSON e salve localmente.

---

## 6. Variáveis de Ambiente

Crie o arquivo .env:

```env
PROJECT_ID=SEU_PROJECT_ID
BUCKET_NAME=SEU_BUCKET_NAME
DATASET_ID=SEU_DATASET_ID

GOOGLE_APPLICATION_CREDENTIALS=credentials/seu-arquivo.json
```

> [!TIP]
> Para isso, utilize o arquivo `.env.example` que deixei como referência.

---

## 🔄️ Fluxo do Pipeline

A execução principal acontece através do arquivo:

```bash
main.py
```

Sendo o fluxo executado:

```bash
download_data()

transform_data()

generate_gold()

upload_to_gcs()

load_to_bigquery()
```

---

## 📐 Camadas Medallion

### 🥉Bronze

Dados brutos obtidos diretamente da fonte.

```text
data/bronze/german.data
```

### 🥈Silver

Dados tratados e padronizados.

```text
data/silver/german_credit_silver.parquet
```

### 🥇Gold

Datasets analíticos.

```text
credit_risk_summary.parquet

purpose_risk_summary.parquet

age_risk_summary.parquet
```

<br>

<p align="left">
<img src="assets\cloudstorage_screenshot.png" width="100%" alt="Cloud Storage" />
</p>

---

## 🔍 BigQuery e Views Analíticas

Após o carregamento o projeto cria as tabelas no Cloud Storege, assim podemos criar as views pro consumo analitico:

### Tabelas

| Tabela |
|----------|
| german_credit_silver |
| credit_risk_summary |
| purpose_risk_summary |
| age_risk_summary |

### Views

| View |
|---------|
| vw_credit_risk_summary |
| vw_purpose_risk_summary |
| vw_age_risk_summary |
| vw_credit_analysis |

> [!IMPORTANT]
> As views não são criadas automaticamente. 
>
>É necessário criar manualmente no BigQuery, onde serão usadas para análises e visualizações no Data Studio (antigo Looker), além de servir como base para as consultas SQL de exemplo que disponibilizei em 'sql/sample_questions.sql'. 
>
>Preferi não criar um script Python pra isso porque queria aprender a mexer mais no BigQuery mesmo, mas se você quiser automatizar, fique à vontade! :)
>
> Pra criar, execute manualmente dentro de uma consulta no BigQuery, o arquivo:
>
> ```text
> sql/create_bigquery_views.sql
> ```


###  Consultas Analíticas

Disponibilizei também algumas consultas de exemplo em:

```bash
sql/sample_questions.sql
```

Exemplos:

- Distribuição de clientes por risco
- Ticket médio por finalidade
- Análise por faixa etária
- Histórico de crédito
- Top maiores empréstimos

<p align="left">
<img src="assets\bigquery_screenshot.png" width="100%" alt="BigQuery" />
</p>

---

## 🗺️ Roadmap

### Próximas Evoluções

- [ ] Provisionamento de infraestrutura com Terraform
- [ ] Deploy automatizado via CI/CD
- [ ] Criação automática das Views via Python
- [ ] Testes automatizados
- [ ] Data Quality Checks
- [ ] Integração com dbt
- [ ] Particionamento e clustering no BigQuery
- [ ] Dashboard com atualização automática

---

## 📈 Sobre a Evolução do Projeto

| Versão | Arquitetura |
|----------|----------|
| V1 | Pipeline local com SQL Server |
| V2 | Pipeline Cloud-Native com GCS + BigQuery + Looker Studio |

A proposta dessa evolução foi transformar um pipeline local em uma solução mais próxima de cenários encontrados em ambientes corporativos modernos de engenharia de dados.

---

> [!IMPORTANT]
> Esse projeto foi desenvolvido apenas com fins educacionais e de portfólio em meus estudos de Engenharia de Dados, Cloud Computing e Analytics.

<p align="center">
  <img src="https://img.shields.io/badge/Feito%20com%20%E2%9D%A4%20por-Millyz%20%20-darkblue" alt="Feito por Millyz">
  <br>
</p>