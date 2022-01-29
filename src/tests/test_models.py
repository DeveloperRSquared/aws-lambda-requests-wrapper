# pylint: disable=no-self-use
import datetime
import json
from typing import Mapping
from typing import Optional

from pydantic import BaseModel

from aws_lambda_requests_wrapper.case_insensitive_dict import CaseInsensitiveDict
from aws_lambda_requests_wrapper.models import Request
from aws_lambda_requests_wrapper.models import Response


class RequestTestCase:
    def create_request(
        self,
        request_id: Optional[str] = None,
        method: Optional[str] = None,
        path: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
        time: Optional[datetime.datetime] = None,
    ) -> Request:
        request_id = request_id or 'request_id'
        method = method or 'POST'
        path = path or '/'
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
    def create_response(
        self,
        body: Optional[str] = None,
        status_code: Optional[int] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Response:
        body = body or 'body'
        status_code = status_code or 200
        headers = headers or {}
        return Response(
            body=body,
            status_code=status_code,
            headers=headers,
        )


class TestFromPydanticModel(ResponseTestCase):
    # check model JSON-ified, status code and headers
    def test_from_pydantic_model(self) -> None:
        class Model(BaseModel):
            model_id: int

        model = Model(model_id=1)
        response = Response.from_pydantic_model(model=model)
        assert response.body == json.dumps(obj={"model_id": 1})
        assert response.status_code == 200
        assert response.headers == {"Content-Type": "application/json"}


class TestToLambdaResponse(ResponseTestCase):
    # check response
    def test_response(self) -> None:
        status_code = 201
        body = json.dumps(obj={"model_id": 1})
        headers = {"accept": "text/html"}
        response = self.create_response(status_code=status_code, body=body, headers=headers)
        lambda_response = response.to_lambda_response()
        assert lambda_response["statusCode"] == status_code
        assert lambda_response["body"] == body
        assert lambda_response["headers"] == headers

    # check headers not in response
    def test_headers_not_returned(self) -> None:
        response = self.create_response()
        response.headers = None
        lambda_response = response.to_lambda_response()
        assert "headers" not in lambda_response
