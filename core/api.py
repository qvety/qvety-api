from ninja import NinjaAPI
from ninja.errors import ValidationError

from common.schemas import ErrorResponse
from qt_auth.api.auth import router as qt_auth_router
from qt_search.api import app as qt_search_app
from qt_space.api.rooms import router as qt_rooms_router

ninja = NinjaAPI()

ninja.add_router('/search/', qt_search_app, tags=['search'])
ninja.add_router('/space/', qt_rooms_router, tags=['space'])
ninja.add_router('/auth/', qt_auth_router, tags=['auth'])


@ninja.exception_handler(ValidationError)
def validation_errors(request, exc):
    errors = exc.errors
    content = ErrorResponse(
        code='BAD_REQUEST',
        detail='Invalid request. Please check the submitted data',
    )

    details = []
    for error in errors:
        field_name = error['loc'][-1]
        msg = error['msg']
        error_data = {field_name: msg}
        details.append(error_data)
    content.errors = details

    return ninja.create_response(request, content, status=400)
