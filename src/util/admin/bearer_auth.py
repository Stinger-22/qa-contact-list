from requests.auth import AuthBase
from requests.models import PreparedRequest


class BearerAuth(AuthBase):
    """Auth implementation for bearer token."""

    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        request.headers["Authorization"] = "Bearer " + self.token
        return request
