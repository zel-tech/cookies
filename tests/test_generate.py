#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate
--------------

Tests for `cookiecutter.generate` module.
"""
from __future__ import unicode_literals
import logging
import os
import shutil
import sys
import unittest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter import exceptions


PY3 = sys.version > '3'

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class TestGenerateFile(unittest.TestCase):

    def test_generate_file(self):
        env = Environment()
        env.loader = FileSystemLoader('.')
        infile = 'tests/files/{{generate_file}}.txt'
        generate.generate_file(
            project_dir=".",
            infile=infile,
            context={'generate_file': 'cheese'},
            env=env
        )
        self.assertTrue(os.path.isfile('tests/files/cheese.txt'))
        with open('tests/files/cheese.txt', 'rt') as f:
             generated_text = f.read()
             self.assertEqual(generated_text, 'Testing cheese')

    def test_generate_file_verbose_template_syntax_error(self):
        env = Environment()
        env.loader = FileSystemLoader('.')
        try:
            generate.generate_file(
                project_dir=".",
                infile='tests/files/syntax_error.txt',
                context={'syntax_error': 'syntax_error'},
                env=env
            )
        except TemplateSyntaxError as exception:
            self.assertEquals(
                str(exception),
                'Missing end of comment tag\n'
                '  File "./tests/files/syntax_error.txt", line 1\n'
                '    I eat {{ syntax_error }} {# this comment is not closed}'
            )
        except exception:
            self.fail('Unexpected exception thrown:', exception)
        else:
            self.fail('TemplateSyntaxError not thrown')

    def tearDown(self):
        if os.path.exists('tests/files/cheese.txt'):
            os.remove('tests/files/cheese.txt')


class TestGenerateFiles(unittest.TestCase):

    def test_generate_files_bad(self):
        self.assertRaises(
            exceptions.NonTemplatedInputDirException,
            generate.generate_files,
            context={'food': 'pizza'},
            template_dir='tests/input'
        )

    def test_generate_files(self):
        generate.generate_files(
            context={'food': 'pizzä'},
            template_dir='tests/input{{food}}'
        )
        self.assertTrue(os.path.isfile('tests/inputpizzä/simple.txt'))
        simple_text = open('tests/inputpizzä/simple.txt', 'rt').read()
        if PY3:
            self.assertEqual(simple_text, 'I eat pizzä')
        else:
            self.assertEqual(simple_text, 'I eat pizzä'.encode('utf-8'))

    def test_generate_files_binaries(self):
        generate.generate_files(
            context={'binary_test': 'binary_files'},
            template_dir='tests/input{{binary_test}}'
        )
        self.assertTrue(os.path.isfile('tests/inputbinary_files/logo.png'))
        self.assertTrue(os.path.isfile('tests/inputbinary_files/.DS_Store'))
        self.assertTrue(os.path.isfile('tests/inputbinary_files/readme.txt'))
        self.assertTrue(
            os.path.isfile('tests/inputbinary_files/some_font.otf')
        )

    def test_generate_binary_files_in_nested_jinja_path(self):
        generate.generate_files(
            context={'binary_test': 'binary_files'},
            template_dir='tests/input{{binary_test}}'
        )
        expected = ['tests/inputbinary_files/binary_files/logo.png',
                    "tests/inputbinary_files/binary_files/.DS_Store",
                    "tests/inputbinary_files/binary_files/readme.txt"]
        for each in expected:
            self.assertTrue(os.path.isfile(each))

    def test_generate_files_absolute_path(self):
        generate.generate_files(
            context={'food': 'pizzä'},
            template_dir=os.path.abspath('tests/input{{food}}')
        )
        self.assertTrue(os.path.isfile('tests/inputpizzä/simple.txt'))

    def tearDown(self):
        if os.path.exists('tests/inputpizzä'):
            shutil.rmtree('tests/inputpizzä')
        if os.path.exists('tests/inputgreen'):
            shutil.rmtree('tests/inputgreen')
        if os.path.exists('tests/inputbinary_files'):
            shutil.rmtree('tests/inputbinary_files')


class TestGenerateContext(unittest.TestCase):

    def test_generate_context(self):
        context = generate.generate_context(config_file='tests/json/test.json')
        self.assertEqual(context, {"test": {"1": 2}})


class TestOutputFolder(unittest.TestCase):

    def test_output_folder(self):
        context = generate.generate_context(
            config_file='tests/json2/stuff.json'
        )
        logging.debug('Context is {0}'.format(context))
        generate.generate_files(
            context=context,
            template_dir='tests/input{{stuff.color}}'
        )

        something = """Hi!
My name is Audrey Greenfeld.
It is 2014."""
        something2 = open('tests/inputgreen/something.txt').read()
        self.assertEqual(something, something2)

        in_folder = "The color is green and the letter is D."
        in_folder2 = open('tests/inputgreen/folder/in_folder.txt').read()
        self.assertEqual(in_folder, in_folder2)

        self.assertTrue(os.path.isdir('tests/inputgreen/im_a.dir'))
        self.assertTrue(os.path.isfile('tests/inputgreen/im_a.dir/im_a.file.py'))

    def tearDown(self):
        if os.path.exists('tests/inputgreen'):
            shutil.rmtree('tests/inputgreen')


class TestHooks(unittest.TestCase):

    def test_ignore_hooks_dirs(self):
        generate.generate_files(
            context={'hooks': 'hooks'},
            template_dir='tests/input{{hooks}}'
        )
        self.assertFalse(os.path.exists('tests/inputhooks/hooks'))

    def test_run_hooks(self):
        generate.generate_files(
            context={'hooks': 'hooks'},
            template_dir='tests/input{{hooks}}'
        )
        self.assertTrue(os.path.exists('tests/inputhooks/foo.txt'))
        self.assertTrue(os.path.exists('tests/inputhooks/bar.txt'))

    def tearDown(self):
        if os.path.exists('tests/inputhooks'):
            shutil.rmtree('tests/inputhooks')


if __name__ == '__main__':
    unittest.main()
