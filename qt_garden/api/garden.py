from django.http import HttpRequest, HttpResponse
from ninja import Router, Schema

from common.exceptions import BaseQtError
from common.http_response import QtORJSONResponse
from common.schemas import ErrorResponse
from qt_auth.logic.jwt_auth_bear import AuthBearer
from qt_garden.logic.garden_service import GardenServie
from qt_garden.schemas.garden import (
    GardenRequestSchema,
    GardenResponseDetailedSchema,
    GardenResponseSchema,
    ListGardenResponseSchema,
)

router = Router()


@router.post(
    path='/plant',
    auth=AuthBearer(),
    response={
        201: GardenResponseSchema,
        (400, 409): ErrorResponse,
    },
)
def create_garden_plant(request: HttpRequest, data: GardenRequestSchema) -> QtORJSONResponse:
    service = GardenServie(request.auth)
    plant = service.create(data)
    return QtORJSONResponse(
        data=GardenResponseSchema.from_orm(plant).model_dump(),
        status=201,
    )


@router.get(
    path='/plants',
    auth=AuthBearer(),
    response={
        200: ListGardenResponseSchema
    },
)
def get_garden_plants_list(request: HttpRequest) -> QtORJSONResponse:
    service = GardenServie(request.auth)
    plants = service.get_list()
    return QtORJSONResponse(
        data=[GardenResponseSchema.from_orm(plant).model_dump() for plant in plants],
        status=200,
    )


@router.get(
    path='/plant/{id}',
    auth=AuthBearer(),
    response={
        200: GardenResponseDetailedSchema,
        404: ErrorResponse,
    },
)
def get_garden_plant_by_id(request: HttpRequest, uid: int) -> QtORJSONResponse:
    service = GardenServie(request.auth)
    try:
        garden = service.get(uid)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=GardenResponseDetailedSchema.from_orm(garden).model_dump(),
        status=200,
    )


@router.put(
    path='/plant/{id}',
    auth=AuthBearer(),
    response={
        201: GardenResponseDetailedSchema,
        404: ErrorResponse,
    },
)
def update_garden_plant_by_id(request, uid: int, data: GardenRequestSchema) -> QtORJSONResponse:
    service = GardenServie(request.auth)
    try:
        plant = service.update(uid, data)
    except BaseQtError as e:
        return e.to_response()

    return QtORJSONResponse(
        data=GardenResponseSchema.from_orm(plant).model_dump(),
        status=201,
    )


@router.delete(
    path='/plant/{id}',
    auth=AuthBearer(),
    response={
        204: Schema,
        404: ErrorResponse,
    },
)
def delete_garden_plant_by_id(request, uid: int) -> HttpResponse:
    service = GardenServie(request.auth)
    try:
        service.delete(uid)
    except BaseQtError as e:
        return e.to_response()
    return HttpResponse(status=204)
