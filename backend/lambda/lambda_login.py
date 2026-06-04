from comum import (
    response,
    get_method,
    get_body,
    find_user_by_email,
    verify_password,
    issue_session,
    users_table,
    now_iso,
)


def lambda_handler(event, context):
    method = get_method(event)
    if method == "OPTIONS":
        return response(200, {})
    if method != "POST":
        return response(405, {"message": "Use POST."})

    body = get_body(event)
    email = str(body.get("email", "")).strip().lower()
    senha = str(body.get("senha", "")).strip()

    if not email or not senha:
        return response(400, {"message": "Informe email e senha."})

    user = find_user_by_email(email)
    if not user:
        return response(401, {"message": "Credenciais inválidas."})

    if not verify_password(senha, user.get("salt", ""), user.get("passwordHash", "")):
        return response(401, {"message": "Credenciais inválidas."})

    token = issue_session(user["userId"])

    users_table.update_item(
        Key={"userId": user["userId"]},
        UpdateExpression="SET lastLoginAt = :lastLoginAt, updatedAt = :updatedAt",
        ExpressionAttributeValues={
            ":lastLoginAt": now_iso(),
            ":updatedAt": now_iso(),
        },
    )

    return response(
        200,
        {
            "token": token,
            "user": {
                "id": user["userId"],
                "nome": user.get("nome", ""),
                "email": user.get("email", ""),
            },
        },
    )
