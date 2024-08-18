import base64
import uuid
from datetime import datetime

import jwt
from django.conf import settings

from common.redis_connection import persistent_client
from qt_auth.logic.exceptions import (
    InvalidJWTRefreshTypeError,
    InvalidPayloadError,
    JWTError,
    JWTExpiredError,
    JWTTokenRevokedError,
    UserNotFoundJWTError,
)
from qt_auth.logic.utils import get_token_secure_key
from qt_user.models import User

ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE = 'access', 'refresh'  # noqa: S105
ALGORITHM_TYPE = 'HS256'
KEY = base64.b64decode(settings.AUTH_KEY)


class JWTService:

    def __init__(self, user: User | None = None):
        self.current_user = user

    def get_user(self) -> User:
        return self.current_user

    def create_access_token(self) -> str:
        return self._create_token(
            user=self.current_user,
            token_type=ACCESS_TOKEN_TYPE,
            exp_delta=settings.AUTH_ACCESS_TOKEN_EXPIRATION,
        )

    def create_refresh_token(self) -> str:
        return self._create_token(
            user=self.current_user,
            token_type=REFRESH_TOKEN_TYPE,
            exp_delta=settings.AUTH_REFRESH_TOKEN_EXPIRATION,
        )

    def verify_access_token(self, token: str) -> None:
        self._get_verify_payload_from_unverified_token(token=token, expected_type=ACCESS_TOKEN_TYPE)

    def verify_refresh_token(self, token: str) -> None:
        verified_payload = self._get_verify_payload_from_unverified_token(token=token, expected_type=REFRESH_TOKEN_TYPE)

        if self._is_token_revoked(verified_payload):
            raise JWTTokenRevokedError()

        self._revoke_token(verified_payload)

    @staticmethod
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

    def _get_verify_payload_from_unverified_token(self, token: str, expected_type: str) -> dict:
        unverified_payload = self._decode_token_payload(token=token, is_verified=False)
        if not (user_id := unverified_payload.get('user_id')):
            raise InvalidPayloadError()

        try:
            user = User.objects.get(id=user_id)
            self._set_user(user)
        except User.DoesNotExist as e:
            raise UserNotFoundJWTError() from e

        verified_payload = self._decode_token_payload(token=token, is_verified=True, user=user)

        if verified_payload['type'] != expected_type:
            # For access token, this error is acceptable (check AuthBear)
            raise InvalidJWTRefreshTypeError()

        return verified_payload

    def _set_user(self, user: User):
        self.current_user = user

    @staticmethod
    def _is_token_revoked(payload: dict) -> bool:
        token_uuid = payload['jti']
        return persistent_client.get(token_uuid) is not None

    @staticmethod
    def _revoke_token(payload: dict) -> None:
        token_uuid = payload['jti']
        exp_time_redis = int(payload['exp'] - datetime.now().timestamp())
        persistent_client.set(token_uuid, 'revoked', ex=exp_time_redis)

    @staticmethod
    def _decode_token_payload(token: str, is_verified: bool, user: User | None = None) -> dict:
        options = {"verify_signature": is_verified}
        key = get_token_secure_key(user) if user and is_verified else None

        try:
            payload = jwt.decode(
                jwt=token,
                key=key,
                algorithms=ALGORITHM_TYPE,
                options=options,
            )
        except (jwt.InvalidSignatureError, jwt.DecodeError) as e:
            raise JWTError() from e
        except jwt.ExpiredSignatureError as e:
            raise JWTExpiredError() from e
        return payload
