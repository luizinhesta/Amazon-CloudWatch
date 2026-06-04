import json
import os
import time
import uuid
import hashlib
import boto3
from boto3.dynamodb.conditions import Key


USERS_TABLE = os.environ.get("USERS_TABLE", "usuarios")
SESSIONS_TABLE = os.environ.get("SESSIONS_TABLE", "sessoes")
SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS", "86400"))

dynamodb = boto3.resource("dynamodb")
users_table = dynamodb.Table(USERS_TABLE)
sessions_table = dynamodb.Table(SESSIONS_TABLE)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def get_method(event):
    if "requestContext" in event:
        method = event.get("requestContext", {}).get("http", {}).get("method")
        if method:
            return method
    return event.get("httpMethod", "")


def get_body(event):
    body = event.get("body")
    if not body:
        return {}
    if isinstance(body, dict):
        return body
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {}


def get_path_param(event, name):
    params = event.get("pathParameters") or {}
    return params.get(name)


def now_epoch():
    return int(time.time())


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def hash_password(password, salt):
    raw = f"{salt}:{password}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def create_user_password(password):
    salt = uuid.uuid4().hex
    return salt, hash_password(password, salt)


def verify_password(password, salt, stored_hash):
    return hash_password(password, salt) == stored_hash


def find_user_by_email(email):
    result = users_table.query(
        IndexName="email-index",
        KeyConditionExpression=Key("email").eq(email),
        Limit=1,
    )
    items = result.get("Items", [])
    return items[0] if items else None


def issue_session(user_id):
    token = uuid.uuid4().hex + uuid.uuid4().hex
    expires_at = now_epoch() + SESSION_TTL_SECONDS
    sessions_table.put_item(
        Item={
            "token": token,
            "userId": user_id,
            "createdAt": now_iso(),
            "expiresAt": expires_at,
        }
    )
    return token


def extract_bearer_token(event):
    headers = event.get("headers") or {}
    auth = headers.get("authorization") or headers.get("Authorization") or ""
    prefix = "Bearer "
    if not auth.startswith(prefix):
        return None
    return auth[len(prefix):].strip()


def validate_session(event):
    token = extract_bearer_token(event)
    if not token:
        return None, response(401, {"message": "Token ausente."})

    session_result = sessions_table.get_item(Key={"token": token})
    session = session_result.get("Item")
    if not session:
        return None, response(401, {"message": "Sessão inválida."})

    if int(session.get("expiresAt", 0)) < now_epoch():
        return None, response(401, {"message": "Sessão expirada."})

    return session, None
