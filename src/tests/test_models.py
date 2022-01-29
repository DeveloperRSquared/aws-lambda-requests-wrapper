# pylint: disable=no-self-use
import datetime
from typing import Mapping
from typing import Optional

from aws_lambda_requests_wrapper.case_insensitive_dict import CaseInsensitiveDict
from aws_lambda_requests_wrapper.models import Request


class RequestTestCase:
    def create_request(
        self,
        request_id: Optional[str] = None,
        method: str = 'POST',
        path: str = '/',
        headers: Optional[Mapping[str, str]] = None,
        time: Optional[datetime.datetime] = None,
    ) -> Request:
        request_id = request_id or 'request_id'
        headers = headers or {}
        time = time or datetime.datetime(2017, 4, 17)
        return Request(
            request_id=request_id,
            method=method,
            path=path,
            headers=headers,
            time=time,
        )


class TestInit(RequestTestCase):
    # check that headers are converted to case-insensitive dict
    def test_case_insensitive_headers(self) -> None:
        request = self.create_request()
        assert isinstance(request.headers, CaseInsensitiveDict)

    # check that headers are converted on assignment
    def test_assigned_headers_case_insensitive(self) -> None:
        request = self.create_request()
        request.headers = {'a': 'b'}
        assert isinstance(request.headers, CaseInsensitiveDict)  # type: ignore[unreachable]


class TestContentType(RequestTestCase):
    # check content type header
    def test_content_type(self) -> None:
        headers = {"Content-Type": "application/json"}
        request = self.create_request(headers=headers)
        assert request.content_type == headers["Content-Type"]

    # check content type header missing
    def test_content_type_missing(self) -> None:
        headers = {"Accept": "application/json"}
        request = self.create_request(headers=headers)
        assert request.content_type is None

    # check content type case insensitive
    def test_content_type_case_insensitive(self) -> None:
        headers = {"Content-TYPE": "application/json"}
        request = self.create_request(headers=headers)
        assert request.content_type == headers["Content-TYPE"]


class TestFromLambdaEvent(RequestTestCase):
    # check that a BadRequest is raised if the version is unsupported
    # check that the all fields are parsed and returned correctly
    # check optional fields missing
    pass


class ResponseTestCase:
    pass


class TestFromPydanticModel(ResponseTestCase):
    # check model JSON-ified, status code and headers
    pass


class TestToLambdaResponse(ResponseTestCase):
    # check response
    # check status code
    # check headers
    pass
