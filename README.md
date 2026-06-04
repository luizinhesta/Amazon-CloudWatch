# 🚀 AWS CloudWatch - Parte 1/1 | Monitorando Aplicações e Serviços AWS

Após construirmos toda a arquitetura da aplicação utilizando serviços AWS como API Gateway, Lambda, DynamoDB e CloudFront, chegou o momento de responder uma das perguntas mais importantes em qualquer ambiente de produção:

Como saber se a aplicação está funcionando corretamente?

Neste primeiro vídeo da série sobre monitoramento, vamos explorar as métricas nativas disponibilizadas pelos principais serviços da AWS e entender quais indicadores devem ser acompanhados diariamente para garantir a disponibilidade, desempenho e estabilidade da aplicação.

![Objetivos](imagens/imagem.jpg)
---
# 🎯 Objetivos

Neste vídeo você aprenderá:

✅ Como acompanhar o tráfego da aplicação

✅ Como identificar erros e falhas de execução

✅ Como analisar métricas de desempenho

✅ Como monitorar a disponibilidade dos serviços

✅ Como interpretar indicadores importantes para operação

✅ Como preparar o ambiente para monitoramentos mais avançados

---

# 🏗️ Arquitetura da Solução

## Front-end

* Amazon S3
* Amazon CloudFront
* Amazon Route 53
* AWS Certificate Manager (ACM)

## Back-end

* Amazon API Gateway
* AWS Lambda
* Amazon DynamoDB
![Objetivos](imagens/imagem%20(11).png)

## Observabilidade

* Amazon CloudWatch
* CloudWatch Dashboards
* CloudWatch Synthetics (Canary)
* CloudWatch RUM

---

# 📂 Estrutura do Projeto

```text
backend/
└── lambda/
    ├── comum.py
    ├── lambda_cadastro.py
    ├── lambda_login.py
    ├── lambda_usuarios.py
    ├── lambda_acesso.py
    ├── policy-lambda-dynamodb-logs.json
    └── policy-lambda-dynamodb-only.json

js/
└── config.js
```

---

# ⚙️ Configuração AWS

## 1. Criar Tabelas DynamoDB

### Tabela `usuarios`

| Configuração  | Valor           |
| ------------- | --------------- |
| Partition Key | userId (String) |
| Capacity Mode | On-Demand       |

### GSI

| Configuração  | Valor          |
| ------------- | -------------- |
| Nome          | email-index    |
| Partition Key | email (String) |

---

### Tabela `sessoes`

| Configuração  | Valor          |
| ------------- | -------------- |
| Partition Key | token (String) |
| Capacity Mode | On-Demand      |

### TTL

```text
Attribute: expiresAt
Status: Enabled
```

---

# 🐍 Funções Lambda

## Funções

| Nome        | Handler                        |
| ----------- | ------------------------------ |
| cw-cadastro | lambda_cadastro.lambda_handler |
| cw-login    | lambda_login.lambda_handler    |
| cw-usuarios | lambda_usuarios.lambda_handler |
| cw-acesso   | lambda_acesso.lambda_handler   |

---

## Configuração

| Item        | Valor           |
| ----------- | --------------- |
| Runtime     | Python 3.12     |
| Memória     | 256 MB          |
| Timeout     | 10 segundos     |
| Arquitetura | x86_64 ou arm64 |

### Variáveis de Ambiente

```env
USERS_TABLE=usuarios
SESSIONS_TABLE=sessoes
SESSION_TTL_SECONDS=86400
```

---

# 📦 Empacotamento

Compacte todos os arquivos da pasta:

```text
backend/lambda/
```

Conteúdo do ZIP:

```text
comum.py
lambda_cadastro.py
lambda_login.py
lambda_usuarios.py
lambda_acesso.py
```

O mesmo pacote pode ser utilizado nas quatro funções Lambda.

---

# 🔐 Permissões IAM

Arquivos disponíveis:

```text
backend/lambda/policy-lambda-dynamodb-logs.json
backend/lambda/policy-lambda-dynamodb-only.json
```

Antes de utilizar:

```text
Substituir:
SEU_ACCOUNT_ID

Pelo ID da sua conta AWS.
```

Após isso:

1. IAM → Policies
2. Create Policy
3. Aba JSON
4. Colar conteúdo
5. Salvar
6. Associar à Role das Lambdas

---

# 🌐 API Gateway

## Criar HTTP API

### Configuração CORS

```text
Allow Origins: *
Allow Methods: GET, POST, PUT, OPTIONS
Allow Headers: *
```

---

## Rotas

| Método | Rota           | Lambda      |
| ------ | -------------- | ----------- |
| POST   | /cadastro      | cw-cadastro |
| POST   | /login         | cw-login    |
| GET    | /usuarios/{id} | cw-usuarios |
| PUT    | /usuarios/{id} | cw-usuarios |
| GET    | /acesso/{id}   | cw-acesso   |

---

## Deploy

```text
Stage: prod
```

---

# 🔧 Configuração Front-end

Arquivo:

```text
js/config.js
```

Alterar:

```javascript
apiBaseUrl: "https://SEU_API_ID.execute-api.us-east-1.amazonaws.com/prod"
```

Para a URL real da API.

---

# ✅ Testes

1. Criar usuário em `cadastro.html`
2. Realizar login em `login.html`
3. Validar acesso em `acesso.html`
4. Atualizar cadastro em `editar-cadastro.html`

---

# 📑 Contrato das APIs

## POST /cadastro

### Request

```json
{
  "nome": "Maria",
  "email": "maria@email.com",
  "senha": "123456"
}
```

---

## POST /login

### Request

```json
{
  "email": "maria@email.com",
  "senha": "123456"
}
```

### Response

```json
{
  "token": "xxxx",
  "user": {
    "id": "uuid",
    "nome": "Maria",
    "email": "maria@email.com"
  }
}
```

---

## PUT /usuarios/{id}

### Header

```text
Authorization: Bearer <token>
```

### Request

```json
{
  "nome": "Maria Silva",
  "email": "maria.silva@email.com"
}
```

---

## GET /acesso/{id}

### Header

```text
Authorization: Bearer <token>
```

---

# 📊 Série CloudWatch

## Vídeo 1 - Monitoramento da Aplicação

Neste vídeo são apresentados os monitoramentos disponíveis nos principais serviços da arquitetura AWS.

### Serviços Monitorados

* CloudFront
* API Gateway
* Lambda
* DynamoDB
* Route 53
* S3

### Métricas Analisadas

#### CloudFront

* Requisições
* Transferência de dados
* Taxa de erros
* Performance

#### Lambda

* Invocações
* Duração
* Erros
* Throttles
* Uso de memória

#### DynamoDB

* Leituras
* Gravações
* Consumo
* Latência
* Throttling

---

## 📸 Fotos do Projeto

<p align="center">
  <img src="imagens/imagem%20(2).png" width="30%" />
  <img src="imagens/imagem%20(3).png" width="30%" />
  <img src="imagens/imagem%20(4).png" width="30%" />
</p>
<p align="center">
  <img src="imagens/imagem%20(5).png" width="30%" />
  <img src="imagens/imagem%20(6).png" width="30%" />
  <img src="imagens/imagem%20(7).png" width="30%" />
</p>
<p align="center">
  <img src="imagens/imagem%20(8).png" width="30%" />
  <img src="imagens/imagem%20(9).png" width="30%" />
  <img src="imagens/imagem%20(10).png" width="30%" />
</p>
<p align="center">
  <img src="imagens/imagem%20(1).png" width="30%" />
</p>


---

# 🚀 Próximos Vídeos

## Parte 2

* CloudWatch Dashboards
* Alarmes
* Notificações

## Parte 3

* CloudWatch Synthetics (Canary)
* CloudWatch RUM

## ▶️ Vídeo do Projeto

Youtube: https://youtu.be/CuBdO9cftM0

Linkedin: https://www.linkedin.com/in/luiz-inhesta-341b4b311/


## 👨‍💻 Autor

**Luiz Augusto Inhesta**

Projeto desenvolvido para estudos, demonstrações práticas e conteúdo técnico sobre AWS.
