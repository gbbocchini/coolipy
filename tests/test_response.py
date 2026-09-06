from coolipy._response import CoolipyAPIResponse


def test_response_holds_data_and_headers():
    resp = CoolipyAPIResponse(status_code=200, data={"a": 1}, headers={"x": "y"})
    assert resp.status_code == 200
    assert resp.data == {"a": 1}
    assert resp.headers == {"x": "y"}


def test_response_headers_default_empty():
    resp = CoolipyAPIResponse(status_code=200, data=None)
    assert resp.headers == {}
