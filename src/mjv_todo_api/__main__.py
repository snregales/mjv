"""Command-line interface."""

import click

from .app import app


@click.command()
@click.option("--host", default="127.0.0.1", help="The hostname to listen on.")
@click.option("--port", default=5000, help="The port to listen on.")
@click.option("--debug", is_flag=True, help="Enable or disable debug mode.")
def run(host, port, debug):
    """Run the Flask application."""
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run(prog_name="mjv-todo-api")  # pragma: no cover
