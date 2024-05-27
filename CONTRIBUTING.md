# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [MIT license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code]
- [Documentation]
- [Issue Tracker]
- [Code of Conduct]

[mit license]: https://opensource.org/licenses/MIT
[source code]: https://github.com/snregales/mjv
[documentation]: https://snregales.github.io/mjv/
[issue tracker]: https://github.com/snregales/mjv/issues

## How to set up your development environment

You need Python 3.11+ and the following tools:

- [Poetry]
- [Nox]
- [nox-poetry]

Install the package with development requirements:

```bash
poetry install
```

You can now run an interactive Python session,
or the command-line interface:

```bash
poetry run python
poetry run mjv-run
```

[poetry]: https://python-poetry.org/
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/

## How to test the project

Run the full test suite:

```bash
nox
```

List the available Nox sessions:

```bash
nox --list-sessions
```

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

```bash
nox --session=tests
```

Unit tests are located in the _tests_ directory,
and are written using the [pytest] testing framework.

[pytest]: https://pytest.readthedocs.io/
