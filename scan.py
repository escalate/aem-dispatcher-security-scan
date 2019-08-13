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
        self.path_list = self.load_path_list('aem-sec-paths.txt')

    def print_configuration(self):
        """Prints configuration of Scan"""
        logging.debug('Website URL is set to "{url}"'.format(
            url=self.website_url))
        logging.debug('Website page path is set to "{path}"'.format(
            path=self.website_page_path))

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
        try:
            r = requests.get(
                url,
                timeout=60)
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
        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=60)
        except requests.exceptions.RequestException as e:
            logging.error('{err} for {url}'.format(err=e, url=url))
        return r

    def perform_all_tests(self):
        """Performs all tests and returns their results"""
        test_results = []
        vulnerabilities_total = 0
        vulnerabilities_hit = 0

        for path in self.path_list:
            r = self.perform_url_test(path.strip())
            test_results.append({'url': r.url, 'status_code': r.status_code})
            vulnerabilities_total += 1
            if r.status_code != requests.codes.not_found:
                vulnerabilities_hit += 1

        r = self.perform_dispatcher_invalidate_cache_test()
        test_results.append({'url': r.url, 'status_code': r.status_code})
        vulnerabilities_total += 1
        if r.status_code != requests.codes.not_found:
            vulnerabilities_hit += 1

        summary = 'Summary: Found {hit} of {total} security relevant AEM Dispatcher URLs'.format(
            hit=vulnerabilities_hit,
            total=vulnerabilities_total)

        return test_results, summary


@click.command()
@click.option('--website-url',
              required=True,
              help='Set URL of website e.g. http://www.adobe.com')
@click.option('--website-page-path',
              help='Set path of website page e.g. /content/geometrixx/en')
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
    scan.print_configuration()

    # Run tests
    click.echo('Start active security scan of URL {website}'.format(
        website=scan.website_url))
    test_results, summary = scan.perform_all_tests()
    for test_result in test_results:
        click.echo('{code}: {url}'.format(
            code=test_result.get('status_code'),
            url=test_result.get('url')
            ))
    click.echo(summary)


if __name__ == '__main__':
    cli()
