# Configuração da Google Cloud Platform

Esse documento descreve todo o processo necessário para configurar a infraestrutura utilizada pelo projeto.

Então eu espero que ao final desse guia você tenha:

- Projeto criado no Google Cloud
- Cloud Storage configurado
- BigQuery configurado
- Service Account criada
- Credenciais JSON geradas
- Variáveis de ambiente configuradas
- Pipeline pronto para execução

> [!NOTE]
> Mas qualquer dúvida, pode me chamar no LinkedIn :)

---

# Visão Geral da Infraestrutura

O projeto utiliza os seguintes serviços:

| Serviço | Finalidade |
|----------|------------|
| Cloud Storage | Armazenamento das camadas Bronze, Silver e Gold |
| BigQuery | Data Warehouse e consultas analíticas |
| IAM | Gerenciamento de permissões |
| Service Account | Autenticação da aplicação |
| Looker Studio | Dashboard analítico |

---

# 1. Criar Projeto no Google Cloud

Acesse:

```text
https://console.cloud.google.com
```

Clique em:

```text
Selecionar Projeto → Novo Projeto
```

Defina:

```text
Nome do Projeto
ID do Projeto
Organização (opcional)
```

Exemplo:

```text
Projeto: credit-risk-platform
ID: credit-risk-platform-499918 (é gerado automaticamente ao dar o nome do projeto)
```

> [!IMPORTANT]
> O ID do projeto deve ser único globalmente. Anote ele pra usar mais tarde.

---

# 2. Habilitar APIs Necessárias

Pelo menu, acesse:

```text
APIs e Serviços → Biblioteca
```

Ative:

### BigQuery API

```text
BigQuery API
```

### Cloud Storage API

```text
Cloud Storage API
```

---

# 3. Criar Bucket no Cloud Storage

Acesse:

```text
Cloud Storage → Buckets
```

Clique em:

```text
Criar Bucket
```

Exemplo utilizado:

```text
credit-risk-platform-bronze-silver-gold
```

Configurações sugeridas:

| Configuração | Valor |
|-------------|--------|
| Região | southamerica-east1(São Paulo) |
| Classe | Standard |
| Controle de acesso | Uniforme |
| Acesso público | Desabilitado |

---

## Estrutura esperada

Após execução do pipeline:

```text
bronze/
silver/
gold/
```

---

### Screenshot

> [!NOTE]
> Deve ficar mais ou menos assim:

<p align="left">
<img src="../assets\cloudstorage_screenshot.png" width="100%" alt="Bucket criado no Cloud Storage" />
</p>

---

# 4. Criar Dataset no BigQuery

Acesse:

```text
BigQuery Studio
```

Clique:

```text
Criar Dataset
```

Configuração:

| Campo | Valor |
|---------|---------|
| Dataset ID | credit_risk |
| Região | southamerica-east1 |

---

### Screenshot

> [!NOTE]
> Depois de criar as views e tudo, deve ficar mais ou menos assim:

<p align="left">
<img src="../assets\bigquery2_screenshot.png" width="100%" alt="Dataset criado no BigQuery" />
</p>


---

# 5. Criar Service Account

Acesse:

```text
IAM e Administração → Contas de Serviço
```

Clique:

```text
Criar Conta de Serviço
```

Descrição:

```text
Conta utilizada pelo pipeline de risco de crédito
```

---

# 6. Conceder Permissões

Adicionar os papéis:

### BigQuery

```text
BigQuery Admin
```

ou

```text
BigQuery Data Editor
BigQuery Job User
```

---

### Cloud Storage

```text
Storage Object Admin
```

---

> [!TIP]
> Em ambiente de produção recomenda-se seguir o princípio do menor privilégio possível, então foi o que tentei seguir aqui.

---

# 7. Gerar Credenciais JSON

Dentro da Service Account:

```text
Chaves → Adicionar Chave
```

Selecionar:

```text
JSON
```

O Google fará download do arquivo.

Exemplo:

```text
project_id-xxxxxxxx.json (nunca compartilhe esse arquivo e evite compartilhar o nome do arquivo também)
```

---

# 8. Criar Pasta credentials

Na raiz do projeto:

```text
credentials/
```

Mover o JSON para dentro:

```text
credentials/service-account.json
```

Estrutura:

```text
credentials/
└── service-account.json
```

---

> [!WARNING]
> Nunca envie esse arquivo para o GitHub.

---

# 9. Configurar Variáveis de Ambiente

Criar arquivo:

```text
.env
```

Exemplo:

```env
PROJECT_ID= id do projeto

BUCKET_NAME= nome do bucket criado no GCS

DATASET_ID= id do dataset criado no BigQuery

REGION= southamerica-east1(São Paulo) ou a região que você escolher

GOOGLE_APPLICATION_CREDENTIALS= credentials/service-account.json
```

---

# 10. Instalar Dependências

Criar ambiente virtual:

```bash
python -m venv .venv
```

Ativar:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

---

# 11. Executar Pipeline

Executar:

```bash
python main.py
```

Resultado esperado:

```text
Pipeline finalizado com sucesso.
```

---

# 12. Criar Views Analíticas

Após o carregamento das tabelas:

Abrir:

```text
sql/create_bigquery_views.sql
```

Executar o script no BigQuery.

Views criadas:

```text
vw_credit_risk_summary
vw_purpose_risk_summary
vw_age_risk_summary
vw_credit_analysis
```

---

# Checklist Final

- [ ] Projeto criado
- [ ] APIs habilitadas
- [ ] Bucket criado
- [ ] Dataset criado
- [ ] Service Account criada
- [ ] Credenciais JSON geradas
- [ ] Arquivo .env configurado
- [ ] Dependências instaladas
- [ ] Pipeline executado
- [ ] Views criadas
- [ ] Dashboard conectado
