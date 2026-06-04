from comum import response, get_method, get_path_param, validate_session, users_table


def lambda_handler(event, context):
    method = get_method(event)
    if method == "OPTIONS":
        return response(200, {})
    if method != "GET":
        return response(405, {"message": "Use GET."})

    session, error_response = validate_session(event)
    if error_response:
        return error_response

    path_user_id = get_path_param(event, "id")
    if not path_user_id:
        return response(400, {"message": "Parâmetro id é obrigatório."})
    if session["userId"] != path_user_id:
        return response(403, {"message": "Você não pode acessar outro usuário."})

    user = users_table.get_item(Key={"userId": path_user_id}).get("Item")
    if not user:
        return response(404, {"message": "Usuário não encontrado."})

    return response(
        200,
        {
            "userId": user["userId"],
            "nome": user.get("nome", ""),
            "email": user.get("email", ""),
            "lastLoginAt": user.get("lastLoginAt"),
            "updatedAt": user.get("updatedAt"),
            "message": "Acesso autorizado.",
        },
    )
