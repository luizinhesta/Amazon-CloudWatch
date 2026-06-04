import uuid
from comum import response, get_method, get_body, users_table, find_user_by_email, create_user_password, now_iso


def lambda_handler(event, context):
    method = get_method(event)
    if method == "OPTIONS":
        return response(200, {})
    if method != "POST":
        return response(405, {"message": "Use POST."})

    body = get_body(event)
    nome = str(body.get("nome", "")).strip()
    email = str(body.get("email", "")).strip().lower()
    senha = str(body.get("senha", "")).strip()

    if not nome or not email or not senha:
        return response(400, {"message": "Informe nome, email e senha."})
    if len(senha) < 6:
        return response(400, {"message": "A senha deve ter no mínimo 6 caracteres."})

    if find_user_by_email(email):
        return response(409, {"message": "Email já cadastrado."})

    user_id = str(uuid.uuid4())
    salt, password_hash = create_user_password(senha)

    users_table.put_item(
        Item={
            "userId": user_id,
            "nome": nome,
            "email": email,
            "salt": salt,
            "passwordHash": password_hash,
            "createdAt": now_iso(),
            "updatedAt": now_iso(),
        }
    )

    return response(201, {"message": "Usuário criado com sucesso.", "userId": user_id})
