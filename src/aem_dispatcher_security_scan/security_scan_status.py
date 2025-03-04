import datetime

import requests


class SecurityScanStatus:
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
        #  True if a vulnerability was found, False otherwise
        self.is_vulnerable = self.is_voulnerability_found(response)

    def is_voulnerability_found(self, response: requests.models.Response):
        """Check if a vulnerability was found in the response

        Returns:
            bool: True if a vulnerability was found, False otherwise
        """
        if response is None:
            return False
        else:
            return response.status_code != requests.codes.not_found

    def __str__(self):
        """Return string representation of the object

        Returns:
            str: String representation of the object
        """
        return "[{time}] {status_code} - {url}".format(
            time=self.time, url=self.url, status_code=self.status_code
        )
