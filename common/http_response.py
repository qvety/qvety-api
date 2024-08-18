import orjson
from django.http.response import HttpResponse


class QtORJSONResponse(HttpResponse):
    def __init__(
            self,
            data: dict | list | None,
            status: int,
            encoder: str | None = None,
            **kwargs,
    ):
        if data is not None:
            data = orjson.dumps(data, default=encoder).decode("utf-8")
        kwargs["content_type"] = "application/json"
        self.status_code = status
        super().__init__(content=data, status=status, **kwargs)
