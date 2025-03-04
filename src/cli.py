#!/usr/bin/env python
import sys

import click
from loguru import logger

from aem_dispatcher_security_scan.security_scanner import SecurityScanner


@click.command()
@click.option(
    "--host",
    required=True,
    default="http://localhost:8080",
    help="Set host of website. "
    "Leave empty to use default value: http://localhost:8080.",
)
@click.option(
    "--page-path",
    default="/content/geometrixx/en",
    help="Set path of website. "
    "Leave empty to use default value: /content/geometrixx/en.",
)
@click.option(
    "--timeout",
    default=10,
    help="Set timeout for http requests in seconds. "
    "Leave emtpy to use default value: 10.",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging output.",
)
def cli(
    host,
    page_path,
    timeout,
    verbose,
):
    """
    Commandline interface for AEM Dispatcher Security Scan
    """

    # Instantiate scan
    scanner = SecurityScanner(host=host, page_path=page_path, request_timeout=timeout)

    # Run security scan
    logger.info(
        "Start active security scan of URL {website}".format(website=scanner.host)
    )

    scanner.validate_all_paths_async()
    results = scanner.results
    total_scans = len(results)

    vulnerable_results = [r for r in results if r.is_vulnerable is True]
    total_vulnerable = len(vulnerable_results)

    # Display results
    if total_vulnerable == 0:
        logger.info(
            "Summary: No security relevant AEM Dispatcher URLs found"
            " in {total} rules.".format(total=total_scans)
        )
        click.exit(0)
    else:
        logger.error(
            "Summary: Found {hit} of {total} security relevant AEM Dispatcher URLs."
            "\n\nVulnerable results are: \n{vulnerable_results}".format(
                hit=total_vulnerable,
                total=total_scans,
                vulnerable_results="\n".join([str(r) for r in vulnerable_results]),
            )
        )
        click.exit(1)


if __name__ == "__main__":
    logger.remove(0)
    logger.add(sys.stdout, format='time={time} level={level} msg="{message}"')
    cli()
