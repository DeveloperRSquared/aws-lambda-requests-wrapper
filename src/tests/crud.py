import json

from aws_lambda_typing.context.context import Context
from aws_lambda_typing.events.api_gateway_proxy import APIGatewayProxyEventV2
from pydantic import BaseModel

from aws_lambda_requests_wrapper.lambda_handler import lambda_request_wrapper
from aws_lambda_requests_wrapper.models import Request
from aws_lambda_requests_wrapper.models import Response


def list_resources_v1(event: APIGatewayProxyEventV2, context: Context) -> str:  # pylint: disable=unused-argument
    return json.dumps({"event": event})


def get_resource_v1(event: APIGatewayProxyEventV2, context: Context) -> str:  # pylint: disable=unused-argument
    return json.dumps({"event": event})


def create_resource_v1(event: APIGatewayProxyEventV2, context: Context) -> str:  # pylint: disable=unused-argument
    return json.dumps({"event": event})


@lambda_request_wrapper()
def list_resources(request: Request) -> Response:
    return Response(body=request.json())


@lambda_request_wrapper()
def get_resource(request: Request) -> Response:
    return Response(body=request.json())


@lambda_request_wrapper()
def get_resource_with_context(request: Request, context: Context) -> Response:  # pylint: disable=unused-argument
    return Response(body=json.dumps({'context': context.function_name}))


@lambda_request_wrapper()
def create_resource(request: Request) -> Response:
    return Response(body=request.json())


class Model(BaseModel):
    model_id: int


@lambda_request_wrapper()
def get_pydantic_model(request: Request) -> Model:  # pylint: disable=unused-argument
    return Model(model_id=1)
