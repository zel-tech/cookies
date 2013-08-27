#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import logging
import os
import shutil
import sys
import unittest

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    input_str = 'builtins.input'
else:
    import __builtin__
    from mock import patch
    input_str = '__builtin__.raw_input'
    from cStringIO import StringIO

from cookiecutter import vcs


# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestVCS(unittest.TestCase):

    def test_git_clone(self):
        repo_dir = vcs.git_clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

    def test_hg_clone(self):
        repo_dir = vcs.hg_clone(
            'https://bitbucket.org/pokoli/cookiecutter-trytonmodule.hg'
        )
        self.assertEqual(repo_dir, 'cookiecutter-trytonmodule')
        self.assertTrue(os.path.isfile('cookiecutter-trytonmodule/README.rst'))
        if os.path.isdir('cookiecutter-trytonmodule'):
            shutil.rmtree('cookiecutter-trytonmodule')


class TestVCSPrompt(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        os.mkdir('cookiecutter-pypackage/')
        if os.path.isdir('cookiecutter-trytonmodule'):
            shutil.rmtree('cookiecutter-trytonmodule')
        os.mkdir('cookiecutter-trytonmodule/')

    @patch(input_str, lambda: 'y')
    def test_git_clone_overwrite(self):
        if not PY3:
            sys.stdin = StringIO('y\n\n')
        repo_dir = vcs.git_clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))

    @patch(input_str, lambda: 'n')
    def test_git_clone_cancel(self):
        if not PY3:
            sys.stdin = StringIO('n\n\n')
        self.assertRaises(
            SystemExit,
            vcs.git_clone,
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )

    @patch(input_str, lambda: 'y')
    def test_hg_clone_overwrite(self):
        if not PY3:
            sys.stdin = StringIO('y\n\n')
        repo_dir = vcs.hg_clone(
            'https://bitbucket.org/pokoli/cookiecutter-trytonmodule.hg'
        )
        self.assertEqual(repo_dir, 'cookiecutter-trytonmodule')
        self.assertTrue(os.path.isfile('cookiecutter-trytonmodule/README.rst'))

    @patch(input_str, lambda: 'n')
    def test_hg_clone_cancel(self):
        if not PY3:
            sys.stdin = StringIO('n\n\n')
        self.assertRaises(
            SystemExit,
            vcs.hg_clone,
            'https://bitbucket.org/pokoli/cookiecutter-trytonmodule.hg'
        )

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('cookiecutter-trytonmodule'):
            shutil.rmtree('cookiecutter-trytonmodule')


if __name__ == '__main__':
    unittest.main()
