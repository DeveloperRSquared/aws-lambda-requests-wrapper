from aws_lambda_requests_wrapper.util import add


def test_add() -> None:
    assert add(first=1, second=1) == 2
