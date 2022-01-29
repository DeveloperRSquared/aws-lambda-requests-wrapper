import inspect
from functools import wraps
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

from http_exceptions.server_exceptions import InternalServerErrorException
from pydantic import BaseModel

if TYPE_CHECKING:
    from aws_lambda_typing.context.context import Context
    from aws_lambda_typing.events.api_gateway_proxy import APIGatewayProxyEventV2
    from aws_lambda_typing.responses.api_gateway_proxy import APIGatewayProxyResponseV2

from aws_lambda_requests_wrapper.models import Request
from aws_lambda_requests_wrapper.models import Response


def lambda_request_wrapper() -> Callable[[Callable[..., Any]], Callable[..., "APIGatewayProxyResponseV2"]]:
    def lambda_request_wrapper_decorator(func: Callable[..., Any]) -> Callable[..., "APIGatewayProxyResponseV2"]:
        @wraps(func)
        def lambda_handler(event: "APIGatewayProxyEventV2", context: "Context") -> "APIGatewayProxyResponseV2":
            kwargs = {}
            if "context" in inspect.getfullargspec(func=func).args:
                kwargs["context"] = context
            request = Request.from_lambda_event(event=event)
            response = func(request=request, **kwargs)
            if isinstance(response, Response):
                pass
            elif isinstance(response, BaseModel):
                response = Response.from_pydantic_model(model=response)
            else:
                raise InternalServerErrorException(message=f"Response type {type(response).__name__!r} not currently supported.")
            return response.to_lambda_response()

        return lambda_handler

    return lambda_request_wrapper_decorator
