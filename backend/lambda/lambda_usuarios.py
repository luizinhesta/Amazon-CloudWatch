from comum import (
    response,
    get_method,
    get_body,
    get_path_param,
    users_table,
    validate_session,
    find_user_by_email,
    now_iso,
)


def lambda_handler(event, context):
    method = get_method(event)
    if method == "OPTIONS":
        return response(200, {})

    session, error_response = validate_session(event)
    if error_response:
        return error_response

    path_user_id = get_path_param(event, "id")
    if not path_user_id:
        return response(400, {"message": "Parâmetro id é obrigatório."})

    if session["userId"] != path_user_id:
        return response(403, {"message": "Você não pode acessar outro usuário."})

    if method == "GET":
        result = users_table.get_item(Key={"userId": path_user_id})
        user = result.get("Item")
        if not user:
            return response(404, {"message": "Usuário não encontrado."})
        return response(
            200,
            {
                "id": user["userId"],
                "nome": user.get("nome", ""),
                "email": user.get("email", ""),
                "createdAt": user.get("createdAt"),
                "updatedAt": user.get("updatedAt"),
                "lastLoginAt": user.get("lastLoginAt"),
            },
        )

    if method == "PUT":
        body = get_body(event)
        nome = str(body.get("nome", "")).strip()
        email = str(body.get("email", "")).strip().lower()
        if not nome or not email:
            return response(400, {"message": "Informe nome e email."})

        user = users_table.get_item(Key={"userId": path_user_id}).get("Item")
        if not user:
            return response(404, {"message": "Usuário não encontrado."})

        existing = find_user_by_email(email)
        if existing and existing["userId"] != path_user_id:
            return response(409, {"message": "Email já está em uso por outro usuário."})

        users_table.update_item(
            Key={"userId": path_user_id},
            UpdateExpression="SET nome = :nome, email = :email, updatedAt = :updatedAt",
            ExpressionAttributeValues={
                ":nome": nome,
                ":email": email,
                ":updatedAt": now_iso(),
            },
        )

        return response(
            200,
            {
                "id": path_user_id,
                "nome": nome,
                "email": email,
            },
        )

    return response(405, {"message": "Método não permitido."})
