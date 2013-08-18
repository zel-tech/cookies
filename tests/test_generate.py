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
import unittest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from cookiecutter import generate
from cookiecutter import exceptions

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class TestGenerate(unittest.TestCase):

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
        self.assertEqual(simple_text, 'I eat pizzä'.encode('utf-8'))

    def test_generate_files_binaries(self):
        generate.generate_files(
            context={'binary_test': 'binary_files'},
            template_dir='tests/input{{binary_test}}'
        )
        self.assertTrue(os.path.isfile('tests/inputbinary_files/logo.png'))
        self.assertTrue(os.path.isfile('tests/inputbinary_files/readme.txt'))
        self.assertTrue(
            os.path.isfile('tests/inputbinary_files/some_font.otf')
        )

    def test_generate_context(self):
        context = generate.generate_context(config_file='tests/json/test.json')
        self.assertEqual(context, {"test": {"1": 2}})

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
        if os.path.exists('tests/inputpizzä'):
            shutil.rmtree('tests/inputpizzä')
        if os.path.exists('tests/inputgreen'):
            shutil.rmtree('tests/inputgreen')
        if os.path.exists('tests/inputbinary_files'):
            shutil.rmtree('tests/inputbinary_files')

if __name__ == '__main__':
    unittest.main()
