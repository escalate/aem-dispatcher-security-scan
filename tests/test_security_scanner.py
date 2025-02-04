import requests
import responses

import unittest

from security_scanner import SecurityScanner

class TestSecurityScanner(unittest.TestCase):
    def test_host_default(self):
        '''
        GIVEN new SecurityScanner object has been created
        WHEN object is created
        THEN host is set to default value
        '''
        scanner = SecurityScanner()

        self.assertEqual(scanner.host, 'http://localhost:8080')

    def test_host_none(self):
        '''
        GIVEN new SecurityScanner object has been created by using None as value of host
        WHEN object is created
        THEN host is set to default value
        '''
        scanner = SecurityScanner(host=None)

        self.assertEqual(scanner.host, 'http://localhost:8080')

    def test_host_custom(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of host
        WHEN object is created
        THEN host is set to value provided in constructor
        '''
        scanner = SecurityScanner(host='http://localhost:8090')

        self.assertEqual(scanner.host, 'http://localhost:8090')

    def test_page_path_default(self):
        '''
        GIVEN new SecurityScanner object has been created
        WHEN object is created
        THEN page_path is set to default value
        '''
        scanner = SecurityScanner()

        self.assertEqual(scanner.page_path, '/content/geometrixx/en')

    def test_page_path_none(self):
        '''
        GIVEN new SecurityScanner object has been created by using None as value of page_path
        WHEN object is created
        THEN page_path is set to default value
        '''
        scanner = SecurityScanner(page_path=None)

        self.assertEqual(scanner.page_path, '/content/geometrixx/en')

    def test_page_path_custom(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of page_path
        WHEN object is created
        THEN page_path is set to value provided in constructor
        '''
        scanner = SecurityScanner(page_path='/content/some-page/en')

        self.assertEqual(scanner.page_path, '/content/some-page/en')

    def test_request_timeout_default(self):
        '''
        GIVEN new SecurityScanner object has been created
        WHEN object is created
        THEN request_timeout is set to default value
        '''
        scanner = SecurityScanner()

        self.assertEqual(scanner.request_timeout, 10)

    def test_request_timeout_none(self):
        '''
        GIVEN new SecurityScanner object has been created by using None as value of request_timeout
        WHEN object is created
        THEN request_timeout is set to default value
        '''
        scanner = SecurityScanner(request_timeout=None)

        self.assertEqual(scanner.request_timeout, 10)

    def test_request_timeout_custom(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of request_timeout
        WHEN object is created
        THEN request_timeout is set to value provided in constructor
        '''
        scanner = SecurityScanner(request_timeout=5)

        self.assertEqual(scanner.request_timeout, 5)

    def test_resource_path_default(self):
        '''
        GIVEN new SecurityScanner object has been created
        WHEN object is created
        THEN paths are loaded from default resource file
        '''
        scanner = SecurityScanner()

        self.assertEqual(620, len(scanner.paths), 'Default security URL list contains 620 paths!')

    def test_resource_path_none(self):
        '''
        GIVEN new SecurityScanner object has been created by using None as value of resource_path
        WHEN object is created
        THEN paths are loaded from default resource file
        '''
        scanner = SecurityScanner(resource_path=None)

        self.assertEqual(620, len(scanner.paths), 'Default security URL list contains 620 paths!')

    def test_load_paths_file_invalid_path(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN load_paths is called with a file that does not exist
        THEN paths are not loaded from the file
        '''
        scanner = SecurityScanner()

        self.assertRaises(FileNotFoundError, scanner.load_paths, resource_path='tests/paths-from-file-not-exist.txt')

    def test_load_paths_file_invalid_extension(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN load_paths is called with a file with invalid extension
        THEN paths are not loaded from the file
        '''
        scanner = SecurityScanner()
        paths = scanner.load_paths(resource_path='tests/paths-from-file.csv')

        self.assertEqual(len(paths), 0)

    def test_load_paths_file_txt(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN load_paths is called with a valid txt file
        THEN paths are loaded from the file
        '''
        scanner = SecurityScanner()
        paths = scanner.load_paths(resource_path='tests/paths-from-file.txt')

        self.assertEqual(len(paths), 3)
        self.assertEqual(paths[0], '/bin/path-from-text-file-1.json')
        self.assertEqual(paths[1], '/bin/path-from-text-file-2.json')
        self.assertEqual(paths[2], '/bin/path-from-text-file-3.json')

    def test_load_paths_file_json(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN load_paths is called with a valid json file
        THEN paths are loaded from the file
        '''
        scanner = SecurityScanner()
        paths = scanner.load_paths(resource_path='tests/paths-from-file.json')

        self.assertEqual(len(paths), 3)
        self.assertEqual(paths[0], '/bin/path-from-json-file-1.json')
        self.assertEqual(paths[1], '/bin/path-from-json-file-2.json')
        self.assertEqual(paths[2], '/bin/path-from-json-file-3.json')

    @responses.activate
    def test_load_paths_from_url_invalid(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN load_paths is called with an invalid URL
        THEN paths are not loaded from the URL
        '''
        responses.add(responses.GET, 'http://localhost:8090/paths-from-url-not-exist.txt', status=404)

        scanner = SecurityScanner()
        paths = scanner.load_paths(resource_path='http://localhost:8090/paths-from-url-not-exist.txt')

        self.assertEqual(len(paths), 0)

    @responses.activate
    def test_load_paths_from_url_txt(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN load_paths is called with a valid URL to a txt file
        THEN paths are loaded from the URL
        '''
        responses.add(responses.GET, 'http://localhost:8090/paths-from-url.txt',
                    body='/bin/path-from-url-1.txt\n/bin/path-from-url-2.txt\n/bin/path-from-url-3.txt',
                    status=200)

        scanner = SecurityScanner()
        paths = scanner.load_paths(resource_path='http://localhost:8090/paths-from-url.txt')

        self.assertEqual(len(paths), 3)
        self.assertEqual(paths[0], '/bin/path-from-url-1.txt')
        self.assertEqual(paths[1], '/bin/path-from-url-2.txt')
        self.assertEqual(paths[2], '/bin/path-from-url-3.txt')

    @responses.activate
    def test_load_paths_from_url_json(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN load_paths is called with a valid URL to a json file
        THEN paths are loaded from the URL
        '''
        responses.add(responses.GET, 'http://localhost:8090/paths-from-url.json',
                    json=['/bin/path-from-url-1.json', '/bin/path-from-url-2.json', '/bin/path-from-url-3.json'],
                    status=200)

        scanner = SecurityScanner()
        paths = scanner.load_paths(resource_path='http://localhost:8090/paths-from-url.json')

        self.assertEqual(len(paths), 3)
        self.assertEqual(paths[0], '/bin/path-from-url-1.json')
        self.assertEqual(paths[1], '/bin/path-from-url-2.json')
        self.assertEqual(paths[2], '/bin/path-from-url-3.json')

    def test_update_path_placeholders(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN update_path_placeholders is called
        THEN paths are updated
        '''
        scanner = SecurityScanner()
 
        paths = [
            '/content/add_valid_path_to_a_page/path-1.txt',
            '/content/add_valid_path_to_a_page/path-2.txt',
            '/content/add_valid_path_to_a_page/path-3.txt'
            ]
        updated_paths = scanner.update_path_placeholders(paths)

        self.assertEqual(len(updated_paths), 3)
        self.assertEqual(updated_paths[0], '/content/geometrixx/en/path-1.txt')
        self.assertEqual(updated_paths[1], '/content/geometrixx/en/path-2.txt')
        self.assertEqual(updated_paths[2], '/content/geometrixx/en/path-3.txt')

    @responses.activate
    def test_retrieve_path_response_invalid_path(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN retrieve_path_response is called with an invalid path
        THEN response is not retrieved
        '''
        responses.add(responses.GET, 'http://localhost:8080/path-not-exist.json', status=404)

        scanner = SecurityScanner()

        status = scanner.retrieve_path_response('/path-not-exist.json')

        self.assertIsNotNone(status)

    @responses.activate
    def test_retrieve_path_response(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN retrieve_path_response is called
        THEN response is retrieved
        '''
        responses.add(responses.GET, 'http://localhost:8090/path.json',
                    body='This is mocked response text.',
                    status=200)

        scanner = SecurityScanner(host='http://localhost:8090', resource_path='tests/paths-from-file.txt')

        status = scanner.retrieve_path_response('/path.json')

        self.assertIsNotNone(status)
        self.assertIsNotNone(status.response)
        self.assertEqual(status.status_code, requests.codes.ok)
        self.assertEqual(status.host, 'http://localhost:8090')
        self.assertEqual(status.path, '/path.json')
        self.assertEqual(status.url, 'http://localhost:8090/path.json')

    @responses.activate
    def test_retrieve_path_response_dispatcher_invalidate(self):
        '''
        GIVEN new SecurityScanner object has been created by using custom value of resource_path
        WHEN retrieve_path_response is called with a path that is invalidated by dispatcher
        THEN response is not retrieved
        '''
        responses.add(responses.GET, 'http://localhost:8090/dispatcher/invalidate.cache',
                    status=200)

        scanner = SecurityScanner(host='http://localhost:8090', resource_path='tests/paths-from-file.txt')

        status = scanner.retrieve_path_response('/dispatcher/invalidate.cache')

        self.assertIsNotNone(status)
        self.assertIsNotNone(status.response)
        self.assertEqual(status.status_code, requests.codes.ok)
        self.assertEqual(status.host, 'http://localhost:8090')
        self.assertEqual(status.path, '/dispatcher/invalidate.cache')
        self.assertEqual(status.url, 'http://localhost:8090/dispatcher/invalidate.cache')
