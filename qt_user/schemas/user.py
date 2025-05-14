import typing as t
from datetime import date

from ninja import Field, Schema

from qt_user.models import User


class UserRequestSchema(Schema):
    first_name: t.Optional[str] = Field(default=None, min_length=2, max_length=150)
    last_name: t.Optional[str] = Field(default=None, min_length=2, max_length=150)
    gender: t.Optional[User.GendersChoices] = None
    bio: t.Optional[str] = None
    birthday: t.Optional[date] = None
    location: t.Optional[str] = Field(default=None, max_length=50)
    hemisphere: t.Optional[User.HemispheresChoices] = None


class UserResponseSchema(Schema):
    email: str
    username: str
    first_name: t.Optional[str]
    last_name: t.Optional[str]
    gender: t.Optional[User.GendersChoices]
    bio: t.Optional[str]
    birthday: t.Optional[date]
    location: t.Optional[str]
    hemisphere: t.Optional[User.HemispheresChoices]
