"""Project Command-line interface."""

from .app import app


def main() -> None:
    """MJV TODO API."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
