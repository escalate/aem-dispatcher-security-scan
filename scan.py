#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Commandline interface to control Scanner class"""

import logging
import click
from security_scan_status import SecurityScanStatus
from security_scanner import SecurityScanner

@click.command()
@click.option(
    '--host',
    required=True,
    default='http://localhost:8080',
    help='Set host of website. Leave empty to use default value: http://localhost:8080.',
)
@click.option(
    '--page-path',
    default='/content/geometrixx/en',
    help='Set path of website. Leave empty to use default value: /content/geometrixx/en.',
)
@click.option(
    '--timeout',
    default=10,
    help='Set timeout for http requests in seconds. Leave emtpy to use default value: 10.',
)

def cli(*args, **kwargs):
    """Commandline interface for AEM Dispatcher Security Scan"""

    # Configure logging
    log_format = '%(levelname)s: %(message)s'
    if kwargs.get('verbose'):
        logging.basicConfig(format=log_format, level=logging.DEBUG)
    else:
        logging.basicConfig(format=log_format)

    # Get arguments
    host = kwargs.get('host')
    page_path = kwargs.get('page_path')
    timeout = kwargs.get('timeout')

    # Instantiate Scan
    scanner = SecurityScanner(host=host, page_path=page_path, request_timeout=timeout)
    
    # Run security scan
    click.echo('Start active security scan of URL {website}\n'.format(
        website=scanner.host))

    #results = scanner.validate_all_paths()
    scanner.validate_all_paths_async()
    results = scanner.results
    total_scans = len(results)

    vulnerable_results = [r for r in results if r.is_vulnerable == True]
    total_vulnerable = len(vulnerable_results)

    # Display results
    if total_vulnerable == 0:
        click.echo('\n\nSummary: No security relevant AEM Dispatcher URLs found in {total} rules.\n'.format(
            total=total_scans))
    else:
        click.echo('\n\nSummary: Found {hit} of {total} security relevant AEM Dispatcher URLs.\n\nVulnerable results are: \n{vulnerable_results}'.format(
            hit=total_vulnerable,
            total=total_scans,
            vulnerable_results='\n'.join([str(r) for r in vulnerable_results])))
        exit(1)
        
if __name__ == '__main__':
    cli()
