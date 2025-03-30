#!/usr/bin/env python

import click

from aem_dispatcher_security_scan.scan_status import ScanStatus
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
def cli(
    host,
    page_path,
    timeout,
):
    """
    Commandline interface for AEM Dispatcher Security Scan
    """

    # Instantiate scan
    scanner = SecurityScanner(host=host, page_path=page_path, request_timeout=timeout)

    # Run security scan
    print(
        "Start active security scan of URL {host}{page_path}".format(
            host=scanner.host, page_path=scanner.page_path
        )
    )

    scanner.validate_all_paths_async()
    results = scanner.results
    total_scans = len(results)

    vulnerable_results = [r for r in results if r.scan_status is ScanStatus.VULNERABLE]
    total_vulnerable = len(vulnerable_results)

    failed_results = [r for r in results if r.scan_status is ScanStatus.FAILED]

    # Display results
    if total_vulnerable == 0:
        print(
            (
                "Summary: No security relevant "
                "AEM Dispatcher URLs found in {total} rules."
            ).format(total=total_scans)
        )
        exit(0)
    else:
        print(
            (
                "Summary: Found {hit} of {total} security relevant "
                "AEM Dispatcher URLs.\n\n"
                "Vulnerable results are: \n{vulnerable_results}"
            ).format(
                hit=total_vulnerable,
                total=total_scans,
                vulnerable_results="\n".join([str(r) for r in vulnerable_results]),
            )
        )
        if len(failed_results) > 0:
            print(
                (
                    "\nPlease check the following URLs manually or re-run scan:"
                    "\n{failed_results}"
                ).format(failed_results="\n".join([str(r) for r in failed_results]))
            )
        exit(1)


if __name__ == "__main__":
    cli()
