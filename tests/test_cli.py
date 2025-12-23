import os
import pytest

from typer.testing import CliRunner
from llamasheets_cli.app import app
from llamasheets_cli.utils import CONFIG_FILE, load_api_key, save_api_key


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    return CliRunner()


def test_auth(runner: CliRunner) -> None:
    if CONFIG_FILE.exists():
        os.remove(CONFIG_FILE)
    result = runner.invoke(app, args=["auth", "--token", "hello"])
    assert result.return_value is None
    assert result.exit_code == 0
    assert "Authentication successful" in result.output.replace("\n", " ").replace(
        "  ", " "
    )
    assert CONFIG_FILE.exists()
    key = load_api_key()
    assert isinstance(key, str)
    assert key == "hello"
    os.remove(CONFIG_FILE)


def test_parse_error(runner: CliRunner) -> None:
    if CONFIG_FILE.exists():
        os.remove(CONFIG_FILE)
    result = runner.invoke(app, args=["parse", "--file", "tests/testfiles/toys.xlsx"])
    assert result.exit_code == 1
    assert "Error: you are not authenticated" in result.output.replace("\n", " ")
    save_api_key(api_key="hello")
    result = runner.invoke(app, args=["parse", "--file", "tests/testfiles/toys.xls"])
    assert result.exit_code == 2
    assert "No such file: tests/testfiles/toys.xls" in result.output.replace("\n", " ")
    result = runner.invoke(app, args=["parse", "--file", "tests/testfiles/toys.xlsx"])
    assert result.exit_code == 3
    assert "An error occured:" in result.output.replace("\n", " ")
    os.remove(CONFIG_FILE)
