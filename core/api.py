from ninja import NinjaAPI
from ninja.errors import ValidationError

from qt_auth.api import app as qt_auth_app
from qt_auth.schemas.auth import ErrorResponse
from qt_search.api import app as qt_search_app

ninja = NinjaAPI()

ninja.add_router('/search/', qt_search_app, tags=['search'])
ninja.add_router('/auth/', qt_auth_app, tags=['auth'])


@ninja.exception_handler(ValidationError)
def validation_errors(request, exc):
    errors = exc.errors
    content = ErrorResponse(
        code='BAD_REQUEST',
        message='Invalid input',
    )

    details = []
    for error in errors:
        field_name = error['loc'][-1]
        msg = error['msg']
        error_data = {field_name: msg}
        details.append(error_data)
    content.errors = details

    return ninja.create_response(request, content, status=400)
