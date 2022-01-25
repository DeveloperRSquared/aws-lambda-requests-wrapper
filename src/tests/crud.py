import json

from aws_lambda_requests_wrapper.lambda_handler import lambda_request_wrapper
from aws_lambda_requests_wrapper.models import Request
from aws_lambda_requests_wrapper.models import Response


def list_resource(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"event": event}),
    }


def get_resource(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"event": event}),
    }


def create_resource(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"event": event}),
    }


@lambda_request_wrapper()
def get_resource_v2(request: Request) -> Response:
    return Response(body="hello")
