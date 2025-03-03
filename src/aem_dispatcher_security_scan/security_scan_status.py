import datetime

import requests


class SecurityScanStatus:
    """
    Class to store the status of a security scan

    Attributes:
        time (datetime): Time when status has been creted
        host (str): Host of the website
        path (str): Path of the website in CRX
        url (str): URL of the website
        response (requests.models.Response): Response object
        status_code (int): Status code of the response
        is_vulnerable (bool): True if a vulnerability was found, False otherwise
    """

    def __init__(self, host, path, response):
        """
        Constructor

            Parameters:
                host (str): Host of the website
                path (str): Path of the website in CRX
                response (requests.models.Response): Response
        """

        self.time = datetime.datetime.now()
        self.host = host
        self.path = path
        self.url = "{host}{path}".format(host=self.host, path=self.path)
        self.response = response
        self.status_code = -1 if response is None else response.status_code
        self.is_vulnerable = self.is_voulnerability_found(response)

    def is_voulnerability_found(self, response):
        """
        Check if a vulnerability was found in the response

                Parameters:
                    response (requests.models.Response): Response object

                Returns:
                    bool: True if a vulnerability was found, False otherwise
        """
        if response is None:
            return False
        else:
            return response.status_code != requests.codes.not_found

    def __str__(self):
        """
        Return string representation of the object

                Returns:
                    str: String representation of the object
        """
        return "[{time}] {status_code} - {url}".format(
            time=self.time, url=self.url, status_code=self.status_code
        )
