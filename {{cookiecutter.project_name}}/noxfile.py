import pathlib

import nox


@nox.session(python=["3.7", "3.8"])
def tests(session):
    session.install("-r", "requirements/tests.txt")
    session.run("pytest", "-v")


@nox.session
def coverage(session):
    session.install("-r", "requirements/tests.txt")
    session.run(
        "pytest",
        "--cov",
        "--cov-report",
        "xml:{toxinidir}/coverage-reports/coverage-all.xml",
    )


@nox.session
def pylint(session):
    session.install("-r", "requirements/develop.txt")
    session.run("pylint", "src/", "tests/", "setup.py")


@nox.session
def pydocstyle(session):
    session.install("pydocstyle")
    session.run("pydocstyle", "src/", "tests/", "setup.py")


@nox.session
def mypy(session):
    session.install("-r", "requirements/develop.txt")
    session.run("mypy", "src/", "tests/", env={"MYPYPATH": "src"})


@nox.session(name="pre-commit")
def pre_commit(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", "--show-diff-on-failure")


@nox.session
def jupyter(session):
    session.install("jupyter", "nbconvert", "nbstripout")
    jupyter_files = [
        str(path) for path in pathlib.Path("jupyter-notebooks").glob("*.ipynb")
    ]
    nbstripout_commands = ["nbstripout"] + jupyter_files
    session.run(*nbstripout_commands)
    jupyter_commands = [
        "jupyter",
        "nbconvert",
        "--execute",
        "--to",
        "notebook",
    ] + jupyter_files
    session.run(*jupyter_commands)
    nbconvert_files = [
        str(path) for path in pathlib.Path("jupyter-notebooks").glob("*nbconvert.*")
    ]
    rm_commands = ["rm"] + nbconvert_files
    session.run(*rm_commands, external=True)
