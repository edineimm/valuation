# 🤖 RPA Framework em Python – Arquitetura Robusta e Escalável

Este repositório contém um **framework de RPA (Robotic Process Automation) desenvolvido em Python**, projetado seguindo **boas práticas de engenharia de software**

## 🎯 Objetivos do Projeto

- Processar **itens de forma isolada**, evitando que falhas interrompam o fluxo  
- Trabalhar com **fila de dados estruturada**  
- Implementar **retry automático**  
- Registrar **status de execução por item**  
- Gerar **dashboard e relatórios**  
- Consolidar resultados em **DataFrames**  
- Facilitar auditoria, reprocessamento e análise de performance  
- Servir como **framework base para RPAs em Python**

---

## ⚙️ Funcionalidades Principais

### ✅ Fila de Itens (Queue)

- Cada item representa uma **unidade independente de trabalho**
- Fila pode ser carregada a partir de:
  - CSV
  - Banco de dados
  - API
- Cada item possui um **Key Item único**

---

### 🔁 Processamento Isolado

- Cada item é processado de forma independente
- Uma falha **não afeta os demais itens**
- Ideal para ambientes instáveis (web, desktop, APIs)

---

### 🔄 Retry Automático

- Número máximo de tentativas configurável
- Tratamento de falhas intermitentes
- Redução de exceções falsas

---

### 🟩🟥 Status de Execução

Cada item finaliza com um status claro:

- `COMPLETO`
- `EXCECAO`

Permite:
- Controle operacional  
- Auditoria  
- Reprocessamento seletivo  

---

### 📊 Dashboard de Execução

- Visão executiva da execução
- Quantidade de itens por status
- Tempo médio de execução
- Gráfico de barras por item (tempo de execução)
- Eixo X com IDs inteiros (auditável)

---

### 📘 Handbook Operacional

- Geração automática de handbook contendo:
  - Key Item
  - Status
  - Mensagem de exceção (se houver)
- Facilita atuação da operação e suporte

---

### 🧾 Consolidação em DataFrame

- Dados gerados por cada item são consolidados ao final
- Estrutura pronta para:
  - CSV
  - Banco de dados
  - Power BI
  - Grafana
  - Machine Learning

---

### ⚡ Execução Paralela

- Suporte a:
  - Execução sequencial
  - ThreadPool (I/O bound)
  - ProcessPool (CPU bound)
- Configuração via variáveis de ambiente

---

### 🔐 Variáveis de Ambiente

- Uso de `.env` para configuração
- Separação de:
  - Paths
  - Flags
  - Parâmetros de execução
- Compatível com múltiplos ambientes (DEV / HOM / PROD)

---

## 🧰 Tecnologias e Ferramentas Utilizadas

- **Python 3.10+**
- **pandas** – manipulação de dados
- **matplotlib** – dashboard e gráficos
- **concurrent.futures** – paralelismo
- **dataclasses** – modelagem de dados
- **python-dotenv** – variáveis de ambiente
- **CSV / DataFrame** – persistência e auditoria

---

## 🔌 Integrações Possíveis

Este framework pode ser facilmente integrado com:

- 🌐 Automação Web (Selenium / Playwright)
- 🖥️ Automação Desktop
- 🔗 APIs REST
- 🧠 Machine Learning
- 📊 Power BI / Grafana
- 🗄️ Bancos de dados (PostgreSQL, SQLite, etc.)
- 🤖 Orquestradores RPA (Blue Prism / UiPath via API)
