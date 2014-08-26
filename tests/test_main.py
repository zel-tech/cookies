#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_main
---------

Tests for `cookiecutter.main` module.
"""

import logging
import os
import sys

from cookiecutter import config, main, utils
from tests import CookiecutterCleanSystemTestCase

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
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

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False


# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestCookiecutterLocalNoInput(CookiecutterCleanSystemTestCase):

    def test_cookiecutter(self):
        main.cookiecutter('tests/fake-repo-pre/', no_input=True)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    def test_cookiecutter_no_slash(self):
        main.cookiecutter('tests/fake-repo-pre', no_input=True)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    def tearDown(self):
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')


class TestCookiecutterLocalWithInput(CookiecutterCleanSystemTestCase):

    @patch(input_str, lambda x: '\n')
    def test_cookiecutter_local_with_input(self):
        if not PY3:
            sys.stdin = StringIO("\n\n\n\n\n\n\n\n\n\n\n\n")

        main.cookiecutter('tests/fake-repo-pre/', no_input=False)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    def tearDown(self):
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')


class TestArgParsing(unittest.TestCase):

    def test_parse_cookiecutter_args(self):
        args = main.parse_cookiecutter_args(['project/'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, None)

    def test_parse_cookiecutter_args_with_branch(self):
        args = main.parse_cookiecutter_args(['project/', '--checkout', 'develop'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, 'develop')


class TestAbbreviationExpansion(unittest.TestCase):

    def test_abbreviation_expansion(self):
        input_dir = main.expand_abbreviations('foo', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(input_dir, 'bar')

    def test_abbreviation_expansion_not_an_abbreviation(self):
        input_dir = main.expand_abbreviations('baz', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(input_dir, 'baz')

    def test_abbreviation_expansion_prefix(self):
        input_dir = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<{0}>'}})
        self.assertEqual(input_dir, '<a>')

    def test_abbreviation_expansion_builtin(self):
        input_dir = main.expand_abbreviations('gh:a', {})
        self.assertEqual(input_dir, 'https://github.com/a.git')

    def test_abbreviation_expansion_override_builtin(self):
        input_dir = main.expand_abbreviations('gh:a', {'abbreviations': {'gh': '<{0}>'}})
        self.assertEqual(input_dir, '<a>')

    def test_abbreviation_expansion_prefix_ignores_suffix(self):
        input_dir = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<>'}})
        self.assertEqual(input_dir, '<>')

    def test_abbreviation_expansion_prefix_not_0_in_braces(self):
        self.assertRaises(
            IndexError,
            main.expand_abbreviations,
            'xx:a',
            {'abbreviations': {'xx': '{1}'}}
        )


@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub/Bitbucket.')
class TestCookiecutterRepoArg(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')
        if os.path.isdir('module_name'):
            utils.rmtree('module_name')
        super(TestCookiecutterRepoArg, self).tearDown()

    # HACK: The *args is because:
    # 1. If the lambda has 1 arg named x, I sometimes get this error:
    #    TypeError: <lambda>() missing 1 required positional argument: 'x'
    # 2. If lambda has no args, I unpredictably get this error:
    #    TypeError: <lambda>() takes 0 positional arguments but 1 was given
    # *args is the best of both worlds.
    # But I am not sure why I started getting these errors for no reason.
    # Any help would be appreciated. -- @audreyr
    @patch(input_str, lambda *args: '')
    def test_cookiecutter_git(self):
        if not PY3:
            # Simulate pressing return 10x.
            # HACK: There are only 9 prompts in cookiecutter-pypackage's
            # cookiecutter.json (http://git.io/b-1MVA) but 10 \n chars here.
            # There was an "EOFError: EOF when reading a line" test fail here
            # out of the blue, which an extra \n fixed. 
            # Not sure why. There shouldn't be an extra prompt to delete 
            # the repo, since CookiecutterCleanSystemTestCase ensured that it
            # wasn't present.
            # It's possibly an edge case in CookiecutterCleanSystemTestCase.
            # Improvements to this would be appreciated. -- @audreyr
            sys.stdin = StringIO('\n\n\n\n\n\n\n\n\n\n')
        main.cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        clone_dir = os.path.join(os.path.expanduser('~/.cookiecutters'), 'cookiecutter-pypackage')
        self.assertTrue(os.path.exists(clone_dir))
        self.assertTrue(os.path.isdir('boilerplate'))
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))
        self.assertTrue(os.path.exists('boilerplate/setup.py'))

    @patch(input_str, lambda x: '')
    def test_cookiecutter_mercurial(self):
        if not PY3:
            sys.stdin = StringIO('\n\n\n\n\n\n\n\n\n')
        main.cookiecutter('https://bitbucket.org/pokoli/cookiecutter-trytonmodule')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        clone_dir = os.path.join(os.path.expanduser('~/.cookiecutters'), 'cookiecutter-trytonmodule')
        self.assertTrue(os.path.exists(clone_dir))
        self.assertTrue(os.path.isdir('module_name'))
        self.assertTrue(os.path.isfile('module_name/README'))
        self.assertTrue(os.path.exists('module_name/setup.py'))


if __name__ == '__main__':
    unittest.main()
