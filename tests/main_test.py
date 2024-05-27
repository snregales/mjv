"""Test cases for the __main__ module."""

from click.testing import CliRunner

from mjv import __main__


def test_cli_run_help(runner: CliRunner) -> None:
    result = runner.invoke(__main__.run, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "--host" in result.output
    assert "--port" in result.output
    assert "--debug" in result.output
