import re
import typing as t

from ninja import Field, Schema
from ninja.errors import ValidationError
from pydantic import field_validator

from qt_auth.logic.utils import clean_email

EMAIL_RE = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


class SignUpRequestSchema(Schema):
    email: str = Field(..., min_length=3, max_length=512)
    username: str = Field(default=None, validate_default=True, min_length=2, max_length=64)
    password: str = Field(..., min_length=8, max_length=64)

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        email = clean_email(value)

        if not re.match(EMAIL_RE, email):
            raise ValidationError([{'loc': ('email',), 'msg': 'Incorrect format'}])
        return email

    @field_validator('username', mode='before')
    def set_empty_username(cls, value: t.Optional[str], values: dict) -> str:
        if value:
            return value

        email = values.data['email']
        local_part, _ = email.lower().split('@')
        return local_part


class SignUpResponseSchema(Schema):
    username: str


class SignInResponseSchema(Schema):
    username: str
    password: str


class JWTRefreshTokenSchema(Schema):
    refresh: str


class JWTTokenSchema(JWTRefreshTokenSchema):
    access: str
