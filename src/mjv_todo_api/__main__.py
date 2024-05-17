"""Project Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """MJV TODO API."""


if __name__ == "__main__":
    main(prog_name="mjv-todo-api")  # pragma: no cover
