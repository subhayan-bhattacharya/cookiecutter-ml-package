"""Setup script."""
import sys

from setuptools import setup

try:
    from semantic_release import setup_hook

    setup_hook(sys.argv)
except ImportError:
    pass

VERSION_TEMPLATE = '''
"""Automatically generated."""
__version__ = {version!r}
'''.lstrip()


setup(
    use_scm_version={
        "write_to": "src/{{ cookiecutter.project_slug }}/version.py",
        "write_to_template": VERSION_TEMPLATE,
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    }
)
