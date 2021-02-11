#!/usr/bin/env python
import os
import importlib
import subprocess


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

INITIAL_COMMIT_MESSAGE = "Empty project"
FIRST_TAG = "v0.0.0"


def package_install(package, install=True):
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        if install:
            pip.main(['install', package])
        else:
            pip.main(['uninstall', package, '-y'])


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def run_shell_command(command: str) -> None:
    commands = command.split(" ")
    process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    for var in out, err:
        if isinstance(var, (str,)):
           print(var.strip())
        else:
            print(var.decode().strip())


def initialize_precommit(source_dir) -> None:
    os.chdir(source_dir)

    for command in ["uninstall", "install"]:
        pre_commit_cmd = f"pre-commit {command}"
        run_shell_command(pre_commit_cmd)


if __name__ == '__main__':
    if 'nox' == '{{ cookiecutter.automated_testing|lower }}':
        tox_file = os.path.join('tox.ini')
        remove_file(tox_file)

    if 'tox' == '{{ cookiecutter.automated_testing|lower }}':
        nox_file = os.path.join('noxfile.py')
        remove_file(nox_file)

    package_install('gitpython')

    import git
    repo = git.Repo.init(PROJECT_DIRECTORY)
    repo.config_writer(config_level="repository").set_value(
        'filter "nbstripout"',
        "extrakeys",
        " ".join(
            ["metadata.language_info.version", "metadata.language_info.pygments_lexer"]
        ),
    ).release()

    repo.index.add(repo.untracked_files)
    repo.index.commit(INITIAL_COMMIT_MESSAGE)
    repo.create_tag(FIRST_TAG)

    package_install('gitpython', install=False)

    package_install('pre-commit')

    initialize_precommit(PROJECT_DIRECTORY)