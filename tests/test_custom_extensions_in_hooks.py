# -*- coding: utf-8 -*-

"""
test_custom_extension_in_hooks.

Tests to ensure custom cookiecutter extensions are properly made available to
pre- and post-gen hooks.
"""

import codecs
import os

import pytest

from cookiecutter import main


@pytest.fixture(
    params=['custom-extension-pre', 'custom-extension-post'],
    ids=['pre_gen_hook', 'post_gen_hook'],
)
def template(request):
    """Fixture. Allows to split pre and post hooks test directories."""
    return 'tests/test-extensions/' + request.param


@pytest.fixture
def output_dir(tmpdir):
    """Fixture. Create and return custom temp directory for test."""
    return str(tmpdir.mkdir('hello'))


@pytest.fixture(autouse=True)
def modify_syspath(monkeypatch):
    """Fixture. Make sure that the custom extension can be loaded."""
    monkeypatch.syspath_prepend('tests/test-extensions/hello_extension')


def test_hook_with_extension(template, output_dir):
    """Verify custom Jinja2 extension correctly work in hooks and file rendering.

    Each file in hooks has simple tests inside and will raise error if not
    correctly rendered.
    """
    project_dir = main.cookiecutter(
        template,
        no_input=True,
        output_dir=output_dir,
        extra_context={'project_slug': 'foobar', 'name': 'Cookiemonster'},
    )

    readme_file = os.path.join(project_dir, 'README.rst')

    with codecs.open(readme_file, encoding='utf8') as f:
        readme = f.read().strip()

    assert readme == 'Hello Cookiemonster!'
