# pylint: disable=unexpected-keyword-arg,no-self-use,no-value-for-parameter,unsubscriptable-object
import datetime
import json
from typing import Dict
from typing import Optional

from aws_lambda_typing.events.api_gateway_proxy import APIGatewayProxyEventV2

from tests.crud import get_pydantic_model
from tests.crud import get_resource


# aws-api-gateway-http-api-request-wrapper
# aws-lambda-api-gateway-request-wrapper
# https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
# https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/sample-apps/nodejs-apig/event-v2.json
class LambdaHandlerTestCase:
    def build_event(
        self,
        method: str = 'POST',
        path: str = '/',
        raw_query_string: str = '',
        query_string_parameters: Optional[Dict[str, str]] = None,
        path_parameters: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIGatewayProxyEventV2:
        datetime.datetime.utcnow()
        if not headers:
            headers = {
                "accept": "text/html",
            }
        event: APIGatewayProxyEventV2 = {
            "version": "2.0",
            "routeKey": f"GET {path}",
            "rawPath": f"{path}",
            "rawQueryString": raw_query_string,
            "cookies": ["moo=baa"],
            "headers": headers,
            "requestContext": {
                "accountId": "1234",
                "apiId": "moo",
                "domainName": "moo.execute-api.eu-west-2.amazonaws.com",
                "domainPrefix": "moo",
                "http": {
                    "method": method,
                    "path": "/",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "1.2.3.4",
                    "userAgent": "curl/7.77.0",
                },
                "requestId": "request_id",
                "routeKey": "GET /",
                "stage": "$default",
                "time": "24/Jan/2022:12:12:57 +0000",
                "timeEpoch": 1643026377063,
            },
            "isBase64Encoded": False,
        }
        if query_string_parameters is not None:
            event["queryStringParameters"] = query_string_parameters
        if path_parameters is not None:
            event["pathParameters"] = path_parameters
        return event


class TestGetResource(LambdaHandlerTestCase):
    # check returning a dictionary
    def test_curl_get(self) -> None:
        event = self.build_event()
        response = get_resource(event=event, context=None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["method"] == "POST"
        assert body["path"] == "/"

    # check returning a pydantic model
    def test_returning_a_pydantic_model(self) -> None:
        event = self.build_event()
        response = get_pydantic_model(event=event, context=None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body == {"model_id": 1}
        assert response["headers"]["Content-Type"] == "application/json"

    # check path params
    def test_path_parameters(self) -> None:
        path_parameters = {"moo": "baa"}
        event = self.build_event(path_parameters=path_parameters)
        response = get_resource(event=event, context=None)
        body = json.loads(response["body"])
        assert body["path_parameters"] == path_parameters

    # check query params
    def test_query_parameters(self) -> None:
        query_string_parameters = {"moo": "baa"}
        event = self.build_event(query_string_parameters=query_string_parameters)
        response = get_resource(event=event, context=None)
        body = json.loads(response["body"])
        assert body["query_string_parameters"] == query_string_parameters
