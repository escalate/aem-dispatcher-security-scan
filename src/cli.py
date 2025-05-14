#!/usr/bin/env python
import asyncio
import sys

import click
from loguru import logger

from aem_dispatcher_security_scan.aem_dispatcher_security_scan import (
    aem_dispatcher_security_scan,
)


@click.command()
@click.option(
    "--url",
    required=True,
    help="URL of website e.g. https://www.example.com",
)
@click.option(
    "--page-path",
    default="/",
    help="Page path of website. e.g. /content/geometrixx/en (Default: /)",
)
@click.option(
    "--timeout",
    default=10,
    help="Timeout for HTTP requests in seconds. (Default: 10)",
)
@click.option(
    "--file",
    default="aem-sec-paths.txt",
    type=click.Path(exists=True),
    help="Text file with test paths. (Default: aem-sec-paths.txt)",
)
def cli(
    url,
    page_path,
    timeout,
    file,
):
    """
    AEM Dispatcher Security Scan
    """

    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        aem_dispatcher_security_scan(
            url=url,
            page_path=page_path,
            timeout=int(timeout),
            file=file,
        )
    )
    loop.close()


if __name__ == "__main__":
    logger.remove(0)
    logger.add(
        sys.stdout,
        level="INFO",
        format='time={time} level={level} msg="{message}"',
    )
    cli()
