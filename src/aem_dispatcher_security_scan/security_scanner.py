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
        host: str = "http://localhost:8080",
        page_path: str = "/content/geometrixx/en",
        request_timeout: int = 10,
        resource_path: str = "aem-sec-paths.txt",
    ):
        """Constructor"""
        # Host of the website.
        self.host = host
        # Path of the website in CRX.
        self.page_path = page_path
        # Timeout for http requests in seconds.
        self.request_timeout = request_timeout
        # Path to the resource containing test patterns.
        self.paths = self.load_paths(resource_path)

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

    def load_paths(self, resource_path: str):
        """Loads path list from resource. Supported file extensions are .txt and .json.

        Returns:
            list: List of paths
        """
        if resource_path is None or resource_path == "":
            logger.error("Resource path is not set")
            return []

        extension = pathlib.Path(resource_path).suffix
        if extension not in VALID_FILE_EXTENSIONS:
            logger.error(
                'Invalid file extension "{extension}". '
                "Valid file extensions are {valid_extensions}.".format(
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

    def update_path_placeholders(self, paths: list):
        """Replaces placeholder '/content/add_valid_path_to_a_page'
        with valid website page path

        Returns:
            list: List of updated paths
        """
        updated_paths = []
        for path in paths:
            if path is not None and path != "":
                p = path.replace("/content/add_valid_path_to_a_page", self.page_path)
                updated_paths.append(p)
        return updated_paths

    def retrieve_path_response(self, path: str, headers: dict = {}):
        """Retrieve a response from the provided path

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
        """Retrieve a response distpacher invalidate cache endpoint

        Returns:
            SecurityScanStatus: Status of the security
        """
        headers = {"CQ-Handle": "/content", "CQ-Path": "/content"}

        return self.retrieve_path_response(
            path="/dispatcher/invalidate.cache", headers=headers
        )

    def validate_all_paths(self):
        """Performs vulnerability test for all paths provided to the scanner

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
