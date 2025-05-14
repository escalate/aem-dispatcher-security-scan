import httpx
import pytest
from click.testing import CliRunner

from cli import cli


@pytest.fixture(scope="function")
def cli_runner():
    return CliRunner()


@pytest.mark.usefixtures("cli_runner")
def test_cli_with_no_parameter(cli_runner):
    actual = cli_runner.invoke(cli, [])
    assert actual.exit_code == 2
    assert "Usage: cli [OPTIONS]" in actual.output
    assert "Error: Missing option '--url'." in actual.output


@pytest.mark.usefixtures("cli_runner")
@pytest.mark.respx(base_url="https://example.com")
def test_cli_with_all_parameters(cli_runner, respx_mock, caplog):
    respx_mock.get("/content.json").mock(return_value=httpx.Response(200))
    respx_mock.get("/content/geometrixx/en.html").mock(return_value=httpx.Response(200))
    respx_mock.get("/welcome").mock(return_value=httpx.Response(200))
    respx_mock.get("/dispatcher/invalidate.cache").mock(
        return_value=httpx.Response(200)
    )

    actual = cli_runner.invoke(
        cli,
        [
            "--url=https://example.com",
            "--page-path=/content/geometrixx/en",
            "--file=tests/fixtures/test-file.txt",
        ],
    )
    assert (
        "URL: 'https://example.com/content.json' Status Code: '200' Error: 'None'"
    ) in caplog.text
    assert (
        "URL: 'https://example.com/content/geometrixx/en.html' "
        "Status Code: '200' Error: 'None'"
    ) in caplog.text
    assert (
        "URL: 'https://example.com/welcome' Status Code: '200' Error: 'None'"
    ) in caplog.text
    assert (
        "URL: 'https://example.com/dispatcher/invalidate.cache' "
        "Status Code: '200' Error: 'None'"
    ) in caplog.text

    assert actual.exit_code == 0
