import aiofiles
import click
from httpx import AsyncClient, HTTPError, codes
from loguru import logger


async def load_path_list(file: str) -> list:
    """
    Loads the path list from a text file

    Returns:
        list: List of paths
    """
    async with aiofiles.open(file, mode="r") as f:
        return await f.readlines()


async def perform_dispatcher_cache_invalidation_test(
    client: AsyncClient, url: str
) -> tuple:
    """
    Performs a dispatcher cache invalidation test

    Returns:
        tuple: status_code, error_msg
    """
    headers = {
        "CQ-Handle": "/content",
        "CQ-Path": "/content",
    }
    try:
        response = await client.get(
            url,
            headers=headers,
        )
        status_code = response.status_code
        headers = response.headers
        error_msg = None
    except HTTPError as e:
        status_code = None
        headers = None
        error_msg = e

    logger.debug(f"URL: '{url}' Status Code: '{status_code}' Error: '{error_msg}'")
    return status_code, headers, error_msg


async def perform_url_test(client: AsyncClient, url: str) -> tuple:
    """
    Performs a URL test

    Returns:
        tuple: status_code, error_msg
    """
    try:
        response = await client.get(url)

        status_code = response.status_code
        headers = response.headers
        error_msg = None
    except HTTPError as e:
        status_code = None
        headers = {}
        error_msg = f"{type(e).__name__} {e}"

    logger.debug(f"URL: '{url}' Status Code: '{status_code}' Error: '{error_msg}'")
    return status_code, headers, error_msg


async def aem_dispatcher_security_scan(
    url: str, page_path: str, timeout: int, file: str
) -> None:
    """
    Performs a security scan of the AEM Dispatcher

    Returns:
        None
    """
    click.echo(
        f"Start AEM Dispatcher security scan with "
        f"URL '{url}' and page path '{page_path}'"
    )

    client = AsyncClient(timeout=timeout)
    path_list = await load_path_list(file=file)

    total_count = 0
    hit_count = 0
    hits = []

    for path in path_list:

        full_url = "{url}{path}".format(
            url=url,
            path=path.strip().replace("/content/add_valid_path_to_a_page", page_path),
        )

        status_code, headers, error_msg = await perform_url_test(
            client=client,
            url=full_url,
        )
        click.echo(".", nl=False)
        total_count += 1

        cache_error = 0
        if headers.get("x-cache") == "Error from cloudfront":
            cache_error = 1

        if (status_code != codes.NOT_FOUND and cache_error == 0) or (
            status_code != codes.OK and cache_error == 1
        ):
            hit_count += 1

            msg = status_code
            if error_msg is not None:
                msg = error_msg

            hits.append(f"URL: {full_url} -> Result: {msg}")

    dispatcher_url = "{url}/dispatcher/invalidate.cache".format(
        url=url,
    )

    status_code, headers, error_msg = await perform_dispatcher_cache_invalidation_test(
        client=client,
        url=dispatcher_url,
    )
    click.echo(".", nl=False)
    total_count += 1

    cache_error = 0
    if headers.get("x-cache") == "Error from cloudfront":
        cache_error = 1

    if (status_code != codes.NOT_FOUND and cache_error == 0) or (
        status_code != codes.OK and cache_error == 1
    ):
        hit_count += 1

        msg = status_code
        if error_msg is not None:
            msg = error_msg

        hits.append(f"URL: {dispatcher_url} -> Result: {msg}")

    click.echo("")
    click.echo(f"{total_count} URLs tested, {hit_count} URLs found")
    click.echo("")
    for hit in hits:
        click.echo(hit)

    await client.aclose()
