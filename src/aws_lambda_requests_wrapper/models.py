from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from typing import Mapping
from typing import Optional

if TYPE_CHECKING:
    from aws_lambda_typing.events.api_gateway_proxy import APIGatewayProxyEventV2
    from aws_lambda_typing.responses.api_gateway_proxy import APIGatewayProxyResponseV2

from case_insensitive_dict import CaseInsensitiveDict
from datetime_helpers.utils import datetime_from_millis
from http_exceptions.client_exceptions import BadRequestException
from pydantic import BaseModel
from pydantic import validator


class Request(BaseModel):
    request_id: str
    method: str
    path: str
    headers: Mapping[str, str]
    time: datetime.datetime
    path_parameters: Optional[Mapping[str, str]] = None
    raw_query_string: Optional[str] = None
    query_string_parameters: Optional[Mapping[str, str]] = None
    data: Optional[str] = None

    @validator('headers', pre=True)
    def validate_headers(cls, value: Mapping[str, str]) -> CaseInsensitiveDict[str]:  # pylint: disable=no-self-argument,no-self-use
        return CaseInsensitiveDict(data=value)

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {
            CaseInsensitiveDict: lambda case_insensitive_dict: dict(case_insensitive_dict._data.values()),  # pylint: disable=protected-access
        }

    @property
    def content_type(self) -> Optional[str]:
        return self.headers.get("Content-Type")

    @classmethod
    def from_lambda_event(cls, event: "APIGatewayProxyEventV2") -> Request:
        if event.get("version") != "2.0":
            # TODO: add support for v1?
            raise BadRequestException(message="aws_lambda_requests_wrapper currently only supports v2 events API Gateway Proxy Events.")
        return cls(
            request_id=event["requestContext"]["requestId"],
            method=event["requestContext"]["http"]["method"],
            path=event["requestContext"]["http"]["path"],
            raw_query_string=event["rawQueryString"] or None,
            path_parameters=event.get("pathParameters"),
            query_string_parameters=event.get("queryStringParameters"),
            headers=CaseInsensitiveDict(event["headers"]),
            data=event.get("body"),
            time=datetime_from_millis(millis=event["requestContext"]["timeEpoch"]),
        )


class Response(BaseModel):
    body: str
    status_code: int = 200
    headers: Optional[Mapping[str, str]] = None

    @classmethod
    def from_pydantic_model(cls, model: BaseModel) -> Response:
        return Response(
            body=model.json(),
            status_code=200,
            headers={"Content-Type": "application/json"},
        )

    def to_lambda_response(self) -> "APIGatewayProxyResponseV2":
        lambda_response: "APIGatewayProxyResponseV2" = {
            "statusCode": self.status_code,
            "body": self.body,
        }
        if self.headers is not None:
            lambda_response["headers"] = dict(self.headers)
        return lambda_response
