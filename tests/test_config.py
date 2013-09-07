#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
-----------

Tests for `cookiecutter.config` module.
"""

import os
import shutil
import sys
import unittest

import yaml

from cookiecutter import config
from cookiecutter.exceptions import ConfigDoesNotExistException, InvalidConfiguration

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestGetConfig(unittest.TestCase):

    def test_get_config(self):
        """ Opening and reading config file """
        conf = config.get_config('tests/test-config/valid-config.yaml')
        expected_conf = {
        	'template_dirs': [
        		'/home/raphi/dev'
        	],
        	'default_context': {
        		"full_name": "Raphi Gaziano",
        		"email": "r.gaziano@gmail.com",
        		"github_username": "raphigaziano"
        	}
        }
        self.assertEqual(conf, expected_conf)

    def test_get_config_does_not_exist(self):
        """
        Check that `exceptions.ConfigDoesNotExistException` is raised when
        attempting to get a non-existent config file.
        """
        self.assertRaises(
            ConfigDoesNotExistException,
            config.get_config,
            'tests/test-config/this-does-not-exist.yaml'
        )

    def test_invalid_config(self):
        """
        An invalid config file should raise an `InvalidConfiguration` exception.
        """
        self.assertRaises(InvalidConfiguration, config.get_config,
                          "tests/test-config/invalid-config.yaml")


class TestGetUserConfig(unittest.TestCase):
    
    def setUp(self):
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, '.cookiecutterrc.backup')
            os.remove(self.user_config_path)

    def tearDown(self):
        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists('.cookiecutterrc.backup'):
            shutil.copy('.cookiecutterrc.backup', self.user_config_path)
            os.remove('.cookiecutterrc.backup')

    def test_get_user_config_valid(self):
        """ Get config from a valid ~/.cookiecutterrc file """
        shutil.copy('tests/test-config/valid-config.yaml', self.user_config_path)
        conf = config.get_user_config()
        expected_conf = {
        	'template_dirs': [
        		'/home/raphi/dev'
        	],
        	'default_context': {
        		"full_name": "Raphi Gaziano",
        		"email": "r.gaziano@gmail.com",
        		"github_username": "raphigaziano"
        	}
        }
        self.assertEqual(conf, expected_conf)

    def test_get_user_config_invalid(self):
        """ Get config from an invalid ~/.cookiecutterrc file """
        shutil.copy('tests/test-config/invalid-config.yaml', self.user_config_path)
        self.assertRaises(InvalidConfiguration, config.get_user_config)

    def test_get_user_config_nonexistent(self):
        """ Get config from a nonexistent ~/.cookiecutterrc file """
        self.assertEqual(config.get_user_config(), None)
        



if __name__ == '__main__':
    unittest.main()
