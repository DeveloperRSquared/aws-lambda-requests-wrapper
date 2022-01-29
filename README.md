# AWS Lambda Requests Wrapper

Request/Response wrapper for AWS Lambda with API Gateway.

[![Build](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/build.yml/badge.svg)](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/build.yml)
[![Publish](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/publish.yml/badge.svg)](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/publish.yml)

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](#aws-lambda-requests-wrapper)
[![PyPI - License](https://img.shields.io/pypi/l/aws-lambda-requests-wrapper.svg)](LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/aws-lambda-requests-wrapper.svg)](https://pypi.org/project/aws-lambda-requests-wrapper)

[![codecov](https://codecov.io/gh/DeveloperRSquared/aws-lambda-requests-wrapper/branch/main/graph/badge.svg?token=UI5ZDDDXXB)](https://codecov.io/gh/DeveloperRSquared/aws-lambda-requests-wrapper)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeveloperRSquared/aws-lambda-requests-wrapper/main.svg)](https://results.pre-commit.ci/latest/github/DeveloperRSquared/aws-lambda-requests-wrapper/main)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Install

Install and update using [pip](https://pypi.org/project/aws-lambda-requests-wrapper/).

```sh
$ pip install -U aws-lambda-requests-wrapper
```

## Example

Converts the lambda_handler syntax:

```py
import json

def lambda_handler(event, context):
    ...
    response = {"key": "value"}
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }
```

into this:

```py
import json

from aws_lambda_requests_wrapper.lambda_handler import lambda_request_wrapper
from aws_lambda_requests_wrapper.models import Request
from aws_lambda_requests_wrapper.models import Response

@lambda_request_wrapper()
def lambda_handler(request: Request) -> Response:
    ...
    response = {"key": "value"}
    return Response(body=json.dumps(response))
```

or return a Pydantic model directly:

```py
from pydantic import BaseModel

from aws_lambda_requests_wrapper.lambda_handler import lambda_request_wrapper
from aws_lambda_requests_wrapper.models import Request

class Model(BaseModel):
    model_id: int

@lambda_request_wrapper()
def get_pydantic_model(request: Request) -> Model:
    return Model(model_id=1)
```

## Contributing

Contributions are welcome via pull requests.

### First time setup

```sh
$ git clone git@github.com:DeveloperRSquared/aws-lambda-requests-wrapper.git
$ cd aws-lambda-requests-wrapper
$ poetry install
$ source .venv/bin/activate
```

Tools including black, mypy etc. will run automatically if you install [pre-commit](https://pre-commit.com) using the instructions below

```sh
$ pre-commit install
$ pre-commit run --all-files
```

### Running tests

```sh
$ poetry run pytest
```

## Links

- Source Code: <https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/>
- PyPI Releases: <https://pypi.org/project/aws-lambda-requests-wrapper/>
- Issue Tracker: <https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/issues/>
