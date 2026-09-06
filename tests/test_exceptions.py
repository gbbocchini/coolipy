from coolipy.exceptions import CoolipyError, CoolipyHTTPError


def test_http_error_carries_status_and_message():
    err = CoolipyHTTPError(404, "Resource not found.")
    assert err.status_code == 404
    assert err.message == "Resource not found."
    assert err.errors is None
    assert err.response is None
    assert str(err) == "404: Resource not found."


def test_http_error_carries_validation_errors():
    err = CoolipyHTTPError(422, "Validation error.", errors={"name": ["required"]})
    assert err.errors == {"name": ["required"]}


def test_http_error_subclasses_coolipy_error():
    assert issubclass(CoolipyHTTPError, CoolipyError)
