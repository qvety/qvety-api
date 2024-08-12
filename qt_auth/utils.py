import base64
import hashlib
import uuid
from datetime import datetime

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from ninja.security import HttpBearer

from common.redis_connection import persistent_client
from qt_auth.exceptions import JWTDecodeError, UserNotFound
from qt_user.models import User

ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE = 'access', 'refresh'  # noqa: S105
ALGORITHM_TYPE = 'HS256'
KEY = base64.b64decode(settings.AUTH_KEY)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            refresh_token_payload = get_verified_payload_from_token(token)
        except (JWTDecodeError, UserNotFound):
            return None

        if refresh_token_payload['type'] != ACCESS_TOKEN_TYPE:
            return None

        user = User.objects.get(pk=refresh_token_payload['user_id'])
        return user


def clean_email(email: str) -> str:
    return email.lstrip().rstrip('\r\t\n. ')


def generate_salt(user: User) -> bytes:
    str_user_id = str(user.id)
    salt = hashlib.sha256(str_user_id.encode('utf-8')).digest()
    return salt[:16]


def get_token_secure_key(user: User) -> str:
    password_bytes = user.password.encode('utf-8')
    user_salt = generate_salt(user)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=user_salt,
        iterations=100000,
        backend=default_backend()
    )

    derived_key = kdf.derive(password_bytes)

    h = hmac.HMAC(KEY, hashes.SHA256(), backend=default_backend())
    h.update(derived_key)
    token = h.finalize()

    return base64.b64encode(token).decode('utf-8')


def create_access_token(user: User) -> str:
    return _create_token(user, token_type=ACCESS_TOKEN_TYPE, exp_delta=settings.AUTH_ACCESS_TOKEN_EXPIRATION)


def create_refresh_token(user: User) -> str:
    return _create_token(user, token_type=REFRESH_TOKEN_TYPE, exp_delta=settings.AUTH_REFRESH_TOKEN_EXPIRATION)


def _create_token(user: User, token_type: str, exp_delta: int) -> str:
    current_timestamp = datetime.now().timestamp()

    token_body = {
        'exp': current_timestamp + exp_delta,
        'iat': current_timestamp,
        'jti': str(uuid.uuid4()),
        'user_id': user.id,
        'type': token_type,
    }
    return jwt.encode(token_body, get_token_secure_key(user), ALGORITHM_TYPE)


def revoke_token(payload: dict) -> None:
    if is_token_revoked(payload):
        return

    token_uuid = payload['jti']
    exp_time = payload['exp']
    current_timestamp = datetime.now().timestamp()
    exp_time_redis = int(exp_time - current_timestamp)

    persistent_client.set(token_uuid, 'revoked', ex=exp_time_redis)


def is_token_revoked(payload: dict) -> bool:
    token_uuid = payload['jti']
    return persistent_client.get(token_uuid) is not None


def get_verified_payload_from_token(token: str) -> dict:
    unverified_payload = _decode_token_payload(token=token, is_verified=False)
    if not (user_id := unverified_payload.get('user_id')):
        raise JWTDecodeError('User id not found in payload')

    try:
        suggested_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise UserNotFound('User dose not exist')

    return _decode_token_payload(token=token, is_verified=True, user=suggested_user)


def _decode_token_payload(token: str, is_verified: bool, user: User | None = None) -> dict:
    key = None
    algorithm = None
    options = {"verify_signature": is_verified}

    if user and is_verified:
        key = get_token_secure_key(user)
        algorithm = ALGORITHM_TYPE

    try:
        payload = jwt.decode(
            jwt=token,
            key=key,
            algorithms=algorithm,
            options=options,
        )
    except (jwt.InvalidSignatureError, jwt.DecodeError):
        raise JWTDecodeError('Token decode error')
    except jwt.ExpiredSignatureError:
        raise JWTDecodeError('Token expired')
    return payload
