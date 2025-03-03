import unittest
from unittest.mock import Mock

import requests

from aem_dispatcher_security_scan.security_scan_status import SecurityScanStatus


class TestSecurityScanStatus(unittest.TestCase):

    def test_host(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of host
        WHEN object is created
        THEN host is set to value provided in constructor
        """
        status = SecurityScanStatus("http://localhost:80", None, None)

        self.assertEqual(status.host, "http://localhost:80")

    def test_path(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of path
        WHEN object is created
        THEN path is set to value provided in constructor
        """
        status = SecurityScanStatus(None, "/content/some-page/en", None)

        self.assertEqual(status.path, "/content/some-page/en")

    def test_url(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of host and path
        WHEN object is created
        THEN url is set to concatenation of host and path
        """
        status = SecurityScanStatus(
            "http://localhost:80", "/content/some-page/en", None
        )

        self.assertEqual(status.url, "http://localhost:80/content/some-page/en")

    def test_response(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of response
        WHEN object is created
        THEN response is set to value provided in constructor
        """
        response = Mock(spec=requests.models.Response)
        response.text = "This is mocked response text."
        response.status_code = 200

        status = SecurityScanStatus(None, None, response)

        self.assertIsNotNone(status.response)
        self.assertEqual("This is mocked response text.", status.response.text)

    def test_response_status_code(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of response
        WHEN object is created
        THEN response status code is set to value provided in constructor
        """
        response = Mock(spec=requests.models.Response)
        response.status_code = 200

        status = SecurityScanStatus(None, None, response)

        self.assertIsNotNone(status.response)
        self.assertEqual(requests.codes.ok, status.status_code)

    def test_is_vulnerable_none(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of response
        WHEN object is created
        THEN is_vulnerable is set to False if response is None
        """
        status = SecurityScanStatus(None, None, None)

        self.assertFalse(
            status.is_vulnerable, "Vulnerability is not found if response is None!"
        )

    def test_is_vulnerable_200(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of response
        WHEN object is created
        THEN is_vulnerable is set to True if response status code is not 404
        """
        response = Mock(spec=requests.models.Response)
        response.status_code = 200

        status = SecurityScanStatus(None, None, response)

        self.assertTrue(
            status.is_vulnerable,
            "Vulnerability is found if path exists (response status code is not 404)!",
        )

    def test_is_vulnerable_404(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom value of response
        WHEN object is created
        THEN is_vulnerable is set to False if response status code is 404
        """
        response = Mock(spec=requests.models.Response)
        response.status_code = 404

        status = SecurityScanStatus(None, None, response)

        self.assertFalse(
            status.is_vulnerable,
            "Vulnerability is not found if path does not exist (response status code is 404)!",
        )

    def test_str(self):
        """
        GIVEN new SecurityScanStatus object has been created by using custom values of host, path and response
        WHEN object is converted to string
        THEN string representation of object is returned in format: [timestamp] status_code - url
        """
        response = Mock(spec=requests.models.Response)
        response.status_code = 200

        status = SecurityScanStatus(
            "http://localhost:80", "/content/some-page/en", response
        )

        self.assertRegex(
            str(status),
            "\[\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d{3,}\] \d{3} \- http://localhost:80/content/some-page/en",
        )
