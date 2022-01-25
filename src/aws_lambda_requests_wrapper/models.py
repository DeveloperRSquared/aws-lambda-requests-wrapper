from __future__ import annotations

import datetime
import json
from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import TypedDict
from typing import Union

from datetime_helpers.utils import datetime_from_millis
from pydantic import BaseModel

from aws_lambda_requests_wrapper.case_insensitive_dict import CaseInsensitiveDict
from aws_lambda_requests_wrapper.case_insensitive_dict import CaseInsensitiveDictEncoder


class LambdaResponse(TypedDict, total=False):
    statusCode: int
    headers: Dict[str, str]
    body: str


class Request(BaseModel):
    method: str
    path: str
    headers: CaseInsensitiveDict
    time: datetime.datetime
    path_parameters: Optional[Mapping[str, str]] = None
    raw_query_string: str
    query_string_parameters: Optional[Mapping[str, str]] = None
    data: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            CaseInsensitiveDict: lambda case_insensitive_dict: json.dumps(case_insensitive_dict, cls=CaseInsensitiveDictEncoder),
        }

    @property
    def content_type(self) -> Optional[str]:
        return self.headers.get("Content-Type")

    @property
    def json_data(self) -> Mapping[str, Any]:
        return json.loads(self.data or '')

    @classmethod
    def from_lambda_event(cls, event: Dict[str, Any]) -> Request:
        return cls(
            time=datetime_from_millis(millis=event["requestContext"]["timeEpoch"]),
            method=event['requestContext']['http']['method'],
            path=event['requestContext']['http']['path'],
            raw_query_string=event['rawQueryString'],
            path_parameters=event.get('pathParameters'),
            query_string_parameters=event.get('queryStringParameters'),
            headers=CaseInsensitiveDict(event['headers']),
            data=event.get('body'),
        )


class Response(BaseModel):
    body: Union[str, BaseModel]
    status_code: Optional[int] = None
    headers: Optional[Dict[str, str]] = None

    def to_lambda_response(self) -> LambdaResponse:
        body = self.body
        if isinstance(body, BaseModel):
            body = body.json()
        lambda_response: LambdaResponse = {
            "statusCode": self.status_code or 200,
            "body": body,
        }
        if self.headers:
            lambda_response['headers'] = self.headers
        return lambda_response
