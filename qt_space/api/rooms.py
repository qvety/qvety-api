import uuid

from django.http import HttpRequest, HttpResponse
from ninja import Router, Schema

from common.exceptions import BaseQtError
from common.http_response import QtORJSONResponse
from common.schemas import ErrorResponse
from qt_auth.logic.jwt_auth_bear import AuthBearer
from qt_space.logic.rooms_service import RoomsServie
from qt_space.schemas.space import ListSpaceResponseSchema, RoomRequestSchema, RoomResponseSchema

router = Router()


@router.post(
    path='/room',
    auth=AuthBearer(),
    response={
        201: RoomResponseSchema,
        (400, 409): ErrorResponse,
    },
)
def create_room(request: HttpRequest, data: RoomRequestSchema) -> QtORJSONResponse:
    service = RoomsServie(request.auth)
    try:
        room = service.create(data)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=RoomResponseSchema.from_orm(room).model_dump(),
        status=201,
    )


@router.get(
    path='/rooms',
    auth=AuthBearer(),
    response={
        200: ListSpaceResponseSchema
    },
)
def get_rooms_list(request: HttpRequest) -> QtORJSONResponse:
    service = RoomsServie(request.auth)
    rooms = service.get_list()
    return QtORJSONResponse(
        data=[RoomResponseSchema.from_orm(room).model_dump() for room in rooms],
        status=200,
    )


@router.get(
    path='/room/{uid}',
    auth=AuthBearer(),
    response={
        200: RoomResponseSchema,
        404: ErrorResponse,
    },
)
def get_room_by_uuid(request: HttpRequest, uid: uuid.UUID) -> QtORJSONResponse:
    service = RoomsServie(request.auth)
    try:
        room = service.get(uid)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=RoomResponseSchema.from_orm(room).model_dump(),
        status=200,
    )


@router.put(
    path='/room/{uid}',
    auth=AuthBearer(),
    response={
        200: RoomResponseSchema,
        404: ErrorResponse,
    },
)
def update_room_by_uuid(request, uid: uuid.UUID, data: RoomRequestSchema) -> QtORJSONResponse:
    service = RoomsServie(request.auth)
    try:
        room = service.update(uid, data)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=RoomResponseSchema.from_orm(room).model_dump(),
        status=201,
    )


@router.delete(
    path='/room/{uid}',
    auth=AuthBearer(),
    response={
        204: Schema,
        404: ErrorResponse,
    },
)
def delete_room_by_uuid(request, uid: uuid.UUID) -> HttpResponse:
    service = RoomsServie(request.auth)
    try:
        service.delete(uid)
    except BaseQtError as e:
        return e.to_response()
    return HttpResponse(status=204)
