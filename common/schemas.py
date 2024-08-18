from ninja import Schema


class ErrorResponseTest(Schema):
    code: str
    detail: str
    error: str = ''
