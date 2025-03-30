import datetime

import requests

from .scan_status import ScanStatus


class ScanResult:
    """Class to store the status of a security scan"""

    def __init__(self, host: str, path: str, response: requests.models.Response):
        """Constructor"""
        # Time when status has been creted
        self.time = datetime.datetime.now()
        # Host of the website
        self.host = host
        # Path of the website in CRX
        self.path = path
        # URL of the website
        self.url = "{host}{path}".format(host=self.host, path=self.path)
        # Response object
        self.response = response
        # Status code of the response
        self.status_code = -1 if response is None else response.status_code
        #  ScanStatus enum to identify if vulnerability was found
        self.scan_status = self.retrive_scan_status(response)

    def retrive_scan_status(self, response: requests.models.Response):
        """Check if a vulnerability was found in the response

        Returns:
            ScanStatus
        """
        if response is None:
            return ScanStatus.FAILED
        else:
            if response.status_code == requests.codes.not_found:
                return ScanStatus.SAFE
            else:
                return ScanStatus.VULNERABLE

    def __str__(self):
        """Return string representation of the object

        Returns:
            str: String representation of the object
        """
        return "[{time}] {status_code} - {url}".format(
            time=self.time, url=self.url, status_code=self.status_code
        )
