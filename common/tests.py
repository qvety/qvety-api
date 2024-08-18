import typing as t

from ninja.testing import TestClient


class AuthenticatedClient(TestClient):
    def request(
            self,
            method: str,
            path: str,
            data: dict | None = None,
            json_data: t.Any = None,
            **request_params: t.Any,
    ):
        request_params['headers'] = {'Authorization': f'Bearer **test_access_token**'}
        return super().request(method, path, data, json_data, **request_params)
