import datetime
from typing import Any
from typing import Dict
from typing import Optional

from tests.crud import get_resource_v2


# aws-api-gateway-http-api-request-wrapper
# aws-lambda-api-gateway-request-wrapper
# https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
# https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/sample-apps/nodejs-apig/event-v2.json
class LambdaHandlerTestCase:
    def build_event(
        self,
        path: str = '/',
        raw_query_string: str = '',
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        datetime.datetime.utcnow()
        event: Dict[str, Any] = {
            "version": "2.0",
            "routeKey": f"GET {path}",
            "rawPath": f"{path}",
            "rawQueryString": raw_query_string,
            "headers": headers,
            "requestContext": {
                "accountId": "606576149573",
                "apiId": "egi37t9q1g",
                "domainName": "egi37t9q1g.execute-api.eu-west-2.amazonaws.com",
                "domainPrefix": "egi37t9q1g",
                "http": {"method": "GET", "path": "/", "protocol": "HTTP/1.1", "sourceIp": "80.3.10.77", "userAgent": "curl/7.77.0"},
                "requestId": "McynciO_rPEEPVQ=",
                "routeKey": "GET /",
                "stage": "$default",
                "time": "24/Jan/2022:12:12:57 +0000",
                "timeEpoch": 1643026377063,
            },
            "isBase64Encoded": False,
        }
        return event


class TestGetResource:
    # check path params
    # check query string
    # check returning a dictionary
    # check returning a pydantic model
    def test_curl_get(self):
        event = {
            "version": "2.0",
            "routeKey": "GET /",
            "rawPath": "/",
            "rawQueryString": "",
            "headers": {
                "accept": "*/*",
                "content-length": "0",
                "host": "egi37t9q1g.execute-api.eu-west-2.amazonaws.com",
                "user-agent": "curl/7.77.0",
                "x-amzn-trace-id": "Root=1-61ee97c9-3862bac90b7b2df20e104ab3",
                "x-forwarded-for": "80.3.10.77",
                "x-forwarded-port": "443",
                "x-forwarded-proto": "https",
            },
            "requestContext": {
                "accountId": "606576149573",
                "apiId": "egi37t9q1g",
                "domainName": "egi37t9q1g.execute-api.eu-west-2.amazonaws.com",
                "domainPrefix": "egi37t9q1g",
                "http": {"method": "GET", "path": "/", "protocol": "HTTP/1.1", "sourceIp": "80.3.10.77", "userAgent": "curl/7.77.0"},
                "requestId": "McynciO_rPEEPVQ=",
                "routeKey": "GET /",
                "stage": "$default",
                "time": "24/Jan/2022:12:12:57 +0000",
                "timeEpoch": 1643026377063,
            },
            "isBase64Encoded": False,
        }

        out = get_resource_v2(event=event, context=None)
        print(out)
