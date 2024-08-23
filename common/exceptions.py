from common.http_response import QtORJSONResponse
from common.schemas import ErrorResponse


class BaseQtError(Exception):
    status: int
    code: str
    detail: str

    def to_response(self) -> QtORJSONResponse:
        return QtORJSONResponse(
            data=ErrorResponse(code=self.code, detail=self.detail).model_dump(),
            status=self.status,
        )
