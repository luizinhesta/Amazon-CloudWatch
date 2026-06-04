# Lambdas de Autenticação e Acesso

Este diretório contém o backend para:

- Login
- Cadastro
- Editar cadastro
- Acesso autenticado

## Arquivos

- `comum.py`: arquivo base com funcoes compartilhadas usadas por todas as lambdas.
  Ele centraliza:
  - resposta HTTP com CORS (`response`)
  - leitura de metodo/body da requisicao
  - conexao com DynamoDB
  - hash e validacao de senha
  - criacao e validacao de sessao por token
- `lambda_cadastro.py`: `POST /cadastro`
- `lambda_login.py`: `POST /login`
- `lambda_usuarios.py`: `GET/PUT /usuarios/{id}`
- `lambda_acesso.py`: `GET /acesso/{id}`

## Variáveis de ambiente

- `USERS_TABLE` (default: `usuarios`)
- `SESSIONS_TABLE` (default: `sessoes`)
- `SESSION_TTL_SECONDS` (default: `86400`)

## Policy IAM pronta

- `policy-lambda-dynamodb.json`

Use essa policy no role de execução das Lambdas (ajustando `SEU_ACCOUNT_ID` e, se necessário, região).

## Segurança implementada

- Senha armazenada com hash SHA-256 + salt aleatório.
- Token de sessão salvo na tabela `sessoes`.
- Expiração de sessão por TTL (`expiresAt`).
- Usuário autenticado só acessa o próprio `userId`.
