import pytest
import requests
import responses

from aem_dispatcher_security_scan.security_scanner import SecurityScanner


def test_host_default():
    """
    GIVEN new SecurityScanner object has been created
    WHEN object is created
    THEN host is set to default value
    """
    actual = SecurityScanner()

    assert actual.host == "http://localhost:8080"


def test_host_custom():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of host
    WHEN object is created
    THEN host is set to value provided in constructor
    """
    actual = SecurityScanner(host="http://localhost:8090")

    assert actual.host == "http://localhost:8090"


def test_page_path_default():
    """
    GIVEN new SecurityScanner object has been created
    WHEN object is created
    THEN page_path is set to default value
    """
    actual = SecurityScanner()

    assert actual.page_path == "/content/geometrixx/en"


def test_page_path_custom():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of page_path
    WHEN object is created
    THEN page_path is set to value provided in constructor
    """
    actual = SecurityScanner(page_path="/content/some-page/en")

    assert actual.page_path == "/content/some-page/en"


def test_request_timeout_default():
    """
    GIVEN new SecurityScanner object has been created
    WHEN object is created
    THEN request_timeout is set to default value
    """
    actual = SecurityScanner()

    assert actual.request_timeout == 10


def test_request_timeout_custom():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of request_timeout
    WHEN object is created
    THEN request_timeout is set to value provided in constructor
    """
    actual = SecurityScanner(request_timeout=5)

    assert actual.request_timeout == 5


def test_resource_path_default():
    """
    GIVEN new SecurityScanner object has been created
    WHEN object is created
    THEN paths are loaded from default resource file
    """
    actual = SecurityScanner()

    assert len(actual.paths) == 620


def test_load_paths_file_invalid_path():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN load_paths is called with a file that does not exist
    THEN paths are not loaded from the file
    """

    with pytest.raises(FileNotFoundError):
        SecurityScanner(resource_path="tests/fixtures/paths-from-file-not-exist.txt")


def test_load_paths_file_invalid_extension():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN load_paths is called with a file with invalid extension
    THEN paths are not loaded from the file
    """
    scanner = SecurityScanner()
    actual_paths = scanner.load_paths(
        resource_path="tests/fixtures/paths-from-file.csv"
    )

    assert len(actual_paths) == 0


def test_load_paths_file_txt():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN load_paths is called with a valid txt file
    THEN paths are loaded from the file
    """
    scanner = SecurityScanner()
    actual_paths = scanner.load_paths(
        resource_path="tests/fixtures/paths-from-file.txt"
    )

    assert len(actual_paths) == 3
    assert actual_paths[0] == "/bin/path-from-text-file-1.json"
    assert actual_paths[1] == "/bin/path-from-text-file-2.json"
    assert actual_paths[2] == "/bin/path-from-text-file-3.json"


def test_load_paths_file_json():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN load_paths is called with a valid json file
    THEN paths are loaded from the file
    """
    scanner = SecurityScanner()
    actual_paths = scanner.load_paths(
        resource_path="tests/fixtures/paths-from-file.json"
    )

    assert len(actual_paths) == 3
    assert actual_paths[0] == "/bin/path-from-json-file-1.json"
    assert actual_paths[1] == "/bin/path-from-json-file-2.json"
    assert actual_paths[2] == "/bin/path-from-json-file-3.json"


@responses.activate
def test_load_paths_from_url_invalid():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN load_paths is called with an invalid URL
    THEN paths are not loaded from the URL
    """
    responses.add(
        responses.GET,
        "http://localhost:8090/paths-from-url-not-exist.txt",
        status=404,
    )

    scanner = SecurityScanner()
    actual_paths = scanner.load_paths(
        resource_path="http://localhost:8090/paths-from-url-not-exist.txt"
    )

    assert len(actual_paths) == 0


@responses.activate
def test_load_paths_from_url_txt():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN load_paths is called with a valid URL to a txt file
    THEN paths are loaded from the URL
    """
    responses.add(
        responses.GET,
        "http://localhost:8090/paths-from-url.txt",
        body=(
            "/bin/path-from-url-1.txt\n"
            "/bin/path-from-url-2.txt\n/bin/path-from-url-3.txt"
        ),
        status=200,
    )

    scanner = SecurityScanner()
    actual_paths = scanner.load_paths(
        resource_path="http://localhost:8090/paths-from-url.txt"
    )

    assert len(actual_paths) == 3
    assert actual_paths[0] == "/bin/path-from-url-1.txt"
    assert actual_paths[1] == "/bin/path-from-url-2.txt"
    assert actual_paths[2] == "/bin/path-from-url-3.txt"


@responses.activate
def test_load_paths_from_url_json():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN load_paths is called with a valid URL to a json file
    THEN paths are loaded from the URL
    """
    responses.add(
        responses.GET,
        "http://localhost:8090/paths-from-url.json",
        json=[
            "/bin/path-from-url-1.json",
            "/bin/path-from-url-2.json",
            "/bin/path-from-url-3.json",
        ],
        status=200,
    )

    scanner = SecurityScanner()
    actual_paths = scanner.load_paths(
        resource_path="http://localhost:8090/paths-from-url.json"
    )

    assert len(actual_paths) == 3
    assert actual_paths[0] == "/bin/path-from-url-1.json"
    assert actual_paths[1] == "/bin/path-from-url-2.json"
    assert actual_paths[2] == "/bin/path-from-url-3.json"


def test_update_path_placeholders():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN update_path_placeholders is called
    THEN paths are updated
    """
    scanner = SecurityScanner()

    paths = [
        "/content/add_valid_path_to_a_page/path-1.txt",
        "/content/add_valid_path_to_a_page/path-2.txt",
        "/content/add_valid_path_to_a_page/path-3.txt",
    ]
    actual_updated_paths = scanner.update_path_placeholders(paths)

    assert len(actual_updated_paths) == 3
    assert actual_updated_paths[0] == "/content/geometrixx/en/path-1.txt"
    assert actual_updated_paths[1] == "/content/geometrixx/en/path-2.txt"
    assert actual_updated_paths[2] == "/content/geometrixx/en/path-3.txt"


@responses.activate
def test_retrieve_path_response_invalid_path():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN retrieve_path_response is called with an invalid path
    THEN response is not retrieved
    """
    responses.add(
        responses.GET, "http://localhost:8080/path-not-exist.json", status=404
    )

    scanner = SecurityScanner()
    actual_status = scanner.retrieve_path_response("/path-not-exist.json")

    assert actual_status is not None


@responses.activate
def test_retrieve_path_response():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN retrieve_path_response is called
    THEN response is retrieved
    """
    responses.add(
        responses.GET,
        "http://localhost:8090/path.json",
        body="This is mocked response text.",
        status=200,
    )

    scanner = SecurityScanner(
        host="http://localhost:8090",
        resource_path="tests/fixtures/paths-from-file.txt",
    )

    actual_status = scanner.retrieve_path_response("/path.json")

    assert actual_status is not None
    assert actual_status.response is not None
    assert actual_status.status_code == requests.codes.ok
    assert actual_status.host == "http://localhost:8090"
    assert actual_status.path == "/path.json"
    assert actual_status.url == "http://localhost:8090/path.json"


@responses.activate
def test_retrieve_path_response_dispatcher_invalidate():
    """
    GIVEN new SecurityScanner object has been created
    by using custom value of resource_path
    WHEN retrieve_path_response is called with a path
    that is invalidated by dispatcher
    THEN response is not retrieved
    """
    responses.add(
        responses.GET,
        "http://localhost:8090/dispatcher/invalidate.cache",
        status=200,
    )

    scanner = SecurityScanner(
        host="http://localhost:8090",
        resource_path="tests/fixtures/paths-from-file.txt",
    )

    actual_status = scanner.retrieve_path_response("/dispatcher/invalidate.cache")

    assert actual_status is not None
    assert actual_status.response is not None
    assert actual_status.status_code == requests.codes.ok
    assert actual_status.host == "http://localhost:8090"
    assert actual_status.path == "/dispatcher/invalidate.cache"
    assert actual_status.url == "http://localhost:8090/dispatcher/invalidate.cache"
