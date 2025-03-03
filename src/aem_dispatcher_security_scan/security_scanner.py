import json
import pathlib
import threading

import requests
from loguru import logger
from security_scan_status import SecurityScanStatus

VALID_FILE_EXTENSIONS = [".txt", ".json"]


class SecurityScanner:
    """Class to perfom an active security scan against a AEM dispatcher"""

    results = []
    counter = 0

    def __init__(
        self,
        host="http://localhost:8080",
        page_path="/content/geometrixx/en",
        request_timeout=10,
        resource_path="aem-sec-paths.txt",
    ):
        """
        Constructor

            Parameters:
                host (str): Host of the website. Default is http://localhost:8080.
                page_path (str): Path of the website in CRX. Default is /content/geometrixx/en.
                request_timeout (int): Timeout for http requests in seconds. Default is 1.
                resource_path (str): Path to the resource containing test patterns. Default is aem-sec-paths.txt.
        """
        self.host = "http://localhost:8080" if host is None else host
        self.page_path = "/content/geometrixx/en" if page_path is None else page_path
        self.request_timeout = 10 if request_timeout is None else request_timeout
        self.paths = self.load_paths(
            "aem-sec-paths.txt" if resource_path is None else resource_path
        )

    def print_configuration(self):
        """Prints configuration of SecurityScanner"""
        logger.debug('Host is set to "{host}"'.format(host=self.host))
        logger.debug(
            'Page path is set to "{page_path}"'.format(page_path=self.page_path)
        )
        logger.debug(
            'Request timeout is set to "{request_timeout}"'.format(
                request_timeout=self.request_timeout
            )
        )

    def load_paths(self, resource_path):
        """
        Loads path list from resource. Supported file extensions are .txt and .json.

                Parameters:
                    resource_path (str): Path to the resource containing test patterns (can be local or remote)

                Returns:
                    list: List of paths
        """
        if resource_path is None or resource_path == "":
            logger.error("Resource path is not set")
            return []

        extension = pathlib.Path(resource_path).suffix
        if extension not in VALID_FILE_EXTENSIONS:
            logger.error(
                'Invalid file extension "{extension}". Valid file extensions are {valid_extensions}.'.format(
                    extension=extension, valid_extensions=VALID_FILE_EXTENSIONS
                )
            )
            return []

        paths = []
        if resource_path.startswith("http://") or resource_path.startswith("https://"):
            r = requests.get(resource_path)
            if r.status_code == requests.codes.ok:
                paths = (
                    r.json() if resource_path.endswith(".json") else r.text.splitlines()
                )
            else:
                logger.error(
                    "Failed to load resource from {resource_path}".format(
                        resource_path=resource_path
                    )
                )
                paths = []
        else:
            with open(resource_path, "r") as file:
                paths = (
                    json.load(file)
                    if resource_path.endswith(".json")
                    else file.readlines()
                )

        for i in range(len(paths)):
            paths[i] = paths[i].strip()
        return self.update_path_placeholders(paths)

    def update_path_placeholders(self, paths):
        """
        Replaces placeholder '/content/add_valid_path_to_a_page' with valid website page path

                Parameters:
                    paths (list): List of paths to be updated

                Returns:
                    list: List of updated paths
        """
        updated_paths = []
        for path in paths:
            if path is not None and path != "":
                p = path.replace("/content/add_valid_path_to_a_page", self.page_path)
                updated_paths.append(p)
        return updated_paths

    def retrieve_path_response(self, path, headers={}):
        """
        Retrieve a response from the provided path

                Parameters:
                    path (str): Path to retrieve response from
                    headers (dict): Headers to be added to the request

                Returns:
                    SecurityScanStatus: Status of the security scan

        """
        url = "{host}{path}".format(host=self.host, path=path)

        try:
            r = requests.get(url, headers=headers, timeout=self.request_timeout)

            return SecurityScanStatus(self.host, path, r)
        except requests.exceptions.RequestException as e:
            logger.error("{error} for {url}".format(error=e, url=url))
        return None

    def retrieve_dispatcher_invalidate_cache_response(self):
        """
        Retrieve a response distpacher invalidate cache endpoint

                Returns:
                    SecurityScanStatus: Status of the security
        """
        headers = {"CQ-Handle": "/content", "CQ-Path": "/content"}

        return self.retrieve_path_response(
            path="/dispatcher/invalidate.cache", headers=headers
        )

    def validate_all_paths(self):
        """
        Performs vulnerability test for all paths provided to the scanner

                    Returns:
                        list: List of results for each path provided to the scanner
        """
        results = []
        count = 0
        for path in self.paths:
            print(
                "\rScanning {count} of {total} paths.".format(
                    count=count, total=len(self.paths)
                ),
                end="",
                flush=True,
            )
            count += 1
            results.append(self.retrieve_path_response(path))
        results.append(self.retrieve_dispatcher_invalidate_cache_response())
        return results

    def retrieve_path_response_async(self, path, lock):
        self.results.append(self.retrieve_path_response(path))
        lock.acquire()
        self.counter += 1
        print(
            "\rScanning {count} of {total} paths.".format(
                count=self.counter, total=len(self.paths)
            ),
            end="",
            flush=True,
        )
        lock.release()

    def validate_all_paths_async(self):
        self.results = []
        self.counter = 0

        lock = threading.Lock()
        threads = []
        for path in self.paths:
            t = threading.Thread(
                target=self.retrieve_path_response_async,
                args=(
                    path,
                    lock,
                ),
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
