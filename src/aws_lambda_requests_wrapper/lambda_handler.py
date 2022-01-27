import inspect
from functools import wraps
from typing import TYPE_CHECKING
from typing import Callable
from typing import Union
from typing import overload

if TYPE_CHECKING:
    from aws_lambda_typing.context.context import Context
    from aws_lambda_typing.events.api_gateway_proxy import APIGatewayProxyEventV2
    from aws_lambda_typing.responses.api_gateway_proxy import APIGatewayProxyResponseV2

from pydantic import BaseModel
from typing_extensions import Protocol

from aws_lambda_requests_wrapper.models import Request
from aws_lambda_requests_wrapper.models import Response


class LambdaHandlerProtocol(Protocol):
    @overload
    def __call__(self, request: Request, context: 'Context') -> Union[Response, BaseModel]:
        ...

    @overload
    def __call__(self, request: Request) -> Union[Response, BaseModel]:
        ...


def lambda_request_wrapper() -> Callable[[LambdaHandlerProtocol], Callable[..., 'APIGatewayProxyResponseV2']]:
    def lambda_request_wrapper_decorator(func: LambdaHandlerProtocol) -> Callable[..., 'APIGatewayProxyResponseV2']:
        @wraps(func)
        def lambda_handler(event: 'APIGatewayProxyEventV2', context: 'Context') -> 'APIGatewayProxyResponseV2':
            kwargs = {}
            if 'context' in inspect.getfullargspec(func):
                kwargs['context'] = context
            request = Request.from_lambda_event(event=event)
            response = func(request=request, **kwargs)
            if isinstance(response, BaseModel) and not isinstance(response, Response):
                response = Response.from_pydantic_model(model=response)
            return response.to_lambda_response()

        return lambda_handler

    return lambda_request_wrapper_decorator
