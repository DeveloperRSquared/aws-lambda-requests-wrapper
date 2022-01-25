import inspect
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import overload

from typing_extensions import Protocol

from aws_lambda_requests_wrapper.models import LambdaResponse
from aws_lambda_requests_wrapper.models import Request
from aws_lambda_requests_wrapper.models import Response


class LambdaHandlerProtocol(Protocol):
    @overload
    def __call__(self, request: Request, context: Any) -> Response:
        ...

    @overload
    def __call__(self, request: Request) -> Response:
        ...


def lambda_request_wrapper() -> Callable[[LambdaHandlerProtocol], Callable[..., LambdaResponse]]:
    def lambda_request_wrapper_decorator(func: LambdaHandlerProtocol) -> Callable[..., LambdaResponse]:
        @wraps(func)
        # TODO(rikhil): use a TypedDict for defining event and context types
        def lambda_handler(event: Dict[str, Any], context: Any) -> LambdaResponse:
            kwargs = {}
            if 'context' in inspect.getfullargspec(func):
                kwargs['context'] = context
            request = Request.from_lambda_event(event=event, **kwargs)
            response = func(request=request)
            return response.to_lambda_response()

        return lambda_handler

    return lambda_request_wrapper_decorator
