import re
from unittest.mock import Mock

import requests

from aem_dispatcher_security_scan.security_scan_status import SecurityScanStatus


def test_host():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of host
    WHEN object is created
    THEN host is set to value provided in constructor
    """
    actual = SecurityScanStatus("http://localhost:80", None, None)

    assert actual.host == "http://localhost:80"


def test_path():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of path
    WHEN object is created
    THEN path is set to value provided in constructor
    """
    actual = SecurityScanStatus(None, "/content/some-page/en", None)

    assert actual.path == "/content/some-page/en"


def test_url():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of host and path
    WHEN object is created
    THEN url is set to concatenation of host and path
    """
    actual = SecurityScanStatus("http://localhost:80", "/content/some-page/en", None)

    assert actual.url == "http://localhost:80/content/some-page/en"


def test_response():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of response
    WHEN object is created
    THEN response is set to value provided in constructor
    """
    response = Mock(spec=requests.models.Response)
    response.text = "This is mocked response text."
    response.status_code = 200

    actual = SecurityScanStatus(None, None, response)

    assert actual.response is not None
    assert actual.response.text == "This is mocked response text."


def test_response_status_code():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of response
    WHEN object is created
    THEN response status code is set to value provided in constructor
    """
    response = Mock(spec=requests.models.Response)
    response.status_code = 200

    actual = SecurityScanStatus(None, None, response)

    assert actual.response is not None
    assert actual.status_code == requests.codes.ok


def test_is_vulnerable_none():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of response
    WHEN object is created
    THEN is_vulnerable is set to False if response is None
    """
    actual = SecurityScanStatus(None, None, None)

    assert actual.is_vulnerable is False


def test_is_vulnerable_200():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of response
    WHEN object is created
    THEN is_vulnerable is set to True if response status code is not 404
    """
    response = Mock(spec=requests.models.Response)
    response.status_code = 200

    actual = SecurityScanStatus(None, None, response)

    assert actual.is_vulnerable is True


def test_is_vulnerable_404():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom value of response
    WHEN object is created
    THEN is_vulnerable is set to False if response status code is 404
    """
    response = Mock(spec=requests.models.Response)
    response.status_code = 404

    actual = SecurityScanStatus(None, None, response)

    assert actual.is_vulnerable is False


def test_str():
    """
    GIVEN new SecurityScanStatus object has been created
    by using custom values of host, path and response
    WHEN object is converted to string
    THEN string representation of object is returned
    in format: [timestamp] status_code - url
    """
    response = Mock(spec=requests.models.Response)
    response.status_code = 200

    actual = SecurityScanStatus(
        "http://localhost:80", "/content/some-page/en", response
    )

    assert re.match(
        r"\[\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d{3,}\] \d{3} \-"
        r" http://localhost:80/content/some-page/en",
        actual,
    )
