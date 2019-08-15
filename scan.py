#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Commandline interface
to control Scan class"""

import requests
import logging
import click


class Scan(object):
    """Class to perfom an active security
    scan against a AEM dispatcher"""

    def __init__(self):
        """Constructor"""
        self.website_url = None
        self.website_page_path = None
        self.request_timeout = None
        self.path_list = self.load_path_list('aem-sec-paths.txt')

    def print_configuration(self):
        """Prints configuration of Scan"""
        logging.debug('Website URL is set to "{url}"'.format(
            url=self.website_url))
        logging.debug('Website page path is set to "{path}"'.format(
            path=self.website_page_path))
        logging.debug('Request timeout is set to "{timeout}"'.format(
            timeout=self.request_timeout))

    @staticmethod
    def load_path_list(file_path):
        """Loads path list from text file"""
        with open(file_path, 'r') as text_file:
            return text_file.readlines()

    def replace_page_path(self, path):
        """Replaces placeholder '/content/add_valid_path_to_a_page'
        with valid website page path"""
        if self.website_page_path is not None:
            return path.replace("/content/add_valid_path_to_a_page",
                                self.website_page_path)
        return path

    def perform_url_test(self, path):
        """Performs a single URL test"""
        url = '{website}{path}'.format(website=self.website_url,
                                       path=self.replace_page_path(path))
        r = None
        try:
            r = requests.get(
                url,
                timeout=self.request_timeout)
        except requests.exceptions.RequestException as e:
            logging.error('{err} for {url}'.format(err=e, url=url))
        return r

    def perform_dispatcher_invalidate_cache_test(self):
        """Performs distpacher invalidate cache test"""
        url = '{website}{path}'.format(website=self.website_url,
                                       path='/dispatcher/invalidate.cache')
        headers = {
            'CQ-Handle': '/content',
            'CQ-Path': '/content',
            }
        r = None
        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=self.request_timeout)
        except requests.exceptions.RequestException as e:
            logging.error('{err} for {url}'.format(err=e, url=url))
        return r

    @staticmethod
    def asses_test_result(status_code):
        """Assesses whether the test result is a hit or not"""
        if status_code != requests.codes.not_found:
            return True
        else:
            return False


@click.command()
@click.option('--website-url',
              required=True,
              help='Set URL of website e.g. http://www.adobe.com')
@click.option('--website-page-path',
              help='Set path of website page e.g. /content/geometrixx/en')
@click.option('--timeout',
              default=10.0,
              help='Set timeout for http requests in secs e.g. 1.5 or 5')
@click.option('--verbose',
              is_flag=True,
              help='Enable verbose logging output')
def cli(*args, **kwargs):
    """Commandline interface for AEM Dispatcher Security Scan"""

    # Configure logging
    log_format = '%(levelname)s: %(message)s'
    if kwargs.get('verbose'):
        logging.basicConfig(format=log_format, level=logging.DEBUG)
    else:
        logging.basicConfig(format=log_format)

    # Instantiate Scan
    scan = Scan()

    # Handle options
    scan.website_url = kwargs.get('website_url')
    scan.website_page_path = kwargs.get('website_page_path')
    scan.request_timeout = kwargs.get('timeout')
    scan.print_configuration()

    # Run tests
    vulnerabilities_total = 0
    vulnerabilities_hit = 0

    click.echo('Start active security scan of URL {website}'.format(
        website=scan.website_url))
    click.echo("")

    for path in scan.path_list:
        r = scan.perform_url_test(path.strip())
        vulnerabilities_total += 1
        if r is not None:
            if scan.asses_test_result(r.status_code):
                vulnerabilities_hit += 1
                click.echo('{code}: {url}'.format(
                    code=r.status_code,
                    url=r.url
                ))

    r = scan.perform_dispatcher_invalidate_cache_test()
    vulnerabilities_total += 1
    if r is not None:
        if scan.asses_test_result(r.status_code):
            vulnerabilities_hit += 1
            click.echo('{code}: {url}'.format(
                code=r.status_code,
                url=r.url
            ))

    click.echo("")
    click.echo('Summary: Found {hit} of {total} security relevant AEM Dispatcher URLs'.format(  # noqa: E501
        hit=vulnerabilities_hit,
        total=vulnerabilities_total))


if __name__ == '__main__':
    cli()
