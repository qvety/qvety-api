from django.http import HttpRequest
from ninja import Router

from common.exceptions import BaseQtError
from common.http_response import QtORJSONResponse
from common.schemas import ErrorResponse
from qt_auth.logic.jwt_auth_bear import AuthBearer
from qt_user.logic.user_service import UserServie
from qt_user.schemas.user import UserRequestSchema, UserResponseSchema

router = Router()


@router.get(
    path='/current',
    auth=AuthBearer(),
    response={
        200: UserResponseSchema,
        404: ErrorResponse,
    },
)
def get_current_user(request: HttpRequest) -> QtORJSONResponse:
    service = UserServie(request.auth)
    try:
        user = service.get_current()
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=UserResponseSchema.from_orm(user).model_dump(),
        status=200,
    )


@router.put(
    path='/update',
    auth=AuthBearer(),
    response={
        201: UserResponseSchema,
        404: ErrorResponse,
    },
)
def update_current_user(request: HttpRequest, data: UserRequestSchema) -> QtORJSONResponse:
    service = UserServie(request.auth)
    try:
        user = service.update_current(data)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=UserResponseSchema.from_orm(user).model_dump(),
        status=201,
    )
