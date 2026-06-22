# Lições Aprendidas

Esse documento registra todos os meus aprendizados técnicos, desafios encontrados e soluções adotadas durante o desenvolvimento do projeto.

---

# 1. Diferença entre Pipeline Local e Cloud-Native

## Aprendizado

Migrar um pipeline local para a nuvem envolve muito mais do que trocar o local onde os arquivos são armazenados.

Foi necessário compreender:

- Autenticação
- Permissões
- Regiões
- Estrutura de armazenamento
- Integração entre serviços

---

# 2. Importância das Regiões no BigQuery

## Problema

Durante a criação das views, ocorreram erros como:

```text
Dataset not found in location US
```

Mesmo com o dataset existente.

## Causa

O dataset foi criado em:

```text
southamerica-east1
```

Mas as consultas estavam sendo executadas na região:

```text
US
```

## Solução

Executar as consultas utilizando a mesma região do dataset removendo os filtros que o BigQuery coloca como padrão.

---

## Aprendizado

BigQuery é sensível à região dos recursos.

---

# 3. Mapeamentos Precisam Ser Consistentes

## Problema

Parte dos dados aparecia como:

```text
A40
A41
A42
```

Enquanto outra parte aparecia como:

```text
car_new
car_used
education
```

## Causa

Os dados passaram por versões diferentes do pipeline durante o desenvolvimento.

## Solução

Atualizar o pipeline e tornar as views resilientes aos dois formatos.

---

## Aprendizado

Views analíticas devem ser preparadas para lidar com possíveis inconsistências históricas dos dados.

---

# 4. Separar Transformação e Visualização

## Aprendizado

Inicialmente parecia mais simples realizar traduções diretamente no dashboard.

Posteriormente ficou claro que:

- Traduções pertencem à camada analítica
- Dashboards devem apenas consumir dados já tratados

---

## Resultado

Foram criadas views específicas para apresentação.

---

# 5. Credenciais Nunca Devem Ir para o GitHub

## Aprendizado

Arquivos JSON de Service Account contêm informações sensíveis.

Itens protegidos:

```text
credentials/
.env
*.json
```

---

## Resultado

A configuração foi adicionada ao `.gitignore`.

---

# 6. Estrutura Medallion Facilita a Evolução

## Aprendizado

Separar Bronze, Silver e Gold torna muito mais fácil:

- Depurar erros
- Evoluir transformações
- Reprocessar dados
- Criar novas análises

---

# 7. Views Facilitam Consumo Analítico

## Aprendizado

Criar uma camada de views reduziu significativamente a complexidade das consultas.

Antes:

```sql
CASE
WHEN ...
```

repetido em várias consultas.

Depois:

```sql
SELECT *
FROM vw_purpose_risk_summary
```

---

# 8. Documentação Economiza Tempo

## Aprendizado

Grande parte dos problemas encontrados poderiam ser resolvidos mais rapidamente caso o processo estivesse documentado desde o início.

Por isso foram criados:

- README.md
- architecture.md
- decisions.md
- gcp_setup.md
- lessons_learned.md

---

# 9. Engenharia de Dados Vai Além do Código

## Aprendizado

O desenvolvimento me mostrou que engenharia de dados envolve:

- Dados
- Infraestrutura
- Cloud
- Segurança
- Governança
- Documentação
- Observabilidade

e não apenas Python ou SQL.

---

# 10. Próximos Passos

Os próximos estudos que podem evoluir esse projeto incluem:

- Terraform
- Docker
- Airflow
- dbt
- GitHub Actions
- Data Quality
- Machine Learning (Modelos Preditivos)

---

# Conclusão

Esse projeto representou a transição de um pipeline local para uma arquitetura cloud-native baseada em serviços da Google Cloud.

Além do desenvolvimento técnico, me proporcionou aprendizado prático sobre:

- Cloud Storage
- BigQuery
- Service Accounts
- Views Analíticas
- Dashboards
- Arquitetura Medallion
- Boas práticas de documentação

> [!IMPORTANT]
> O principal aprendizado foi entender que construir pipelines de dados envolve muito mais do que mover dados de um lugar para outro. É necessário pensar em arquitetura, manutenção, reprodutibilidade, segurança e consumo analítico desde o início.