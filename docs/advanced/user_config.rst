.. _user-config:

User Config (0.7.0+)
====================

If you use Cookiecutter a lot, you'll find it useful to have a user config
file. By default Cookiecutter tries to retrieve settings from a `.cookiecutterrc`
file in your home directory.

From version 1.3.0 you can also specify a config file on the command line via ``--config-file``::

    $ cookiecutter --config-file /home/audreyr/my-custom-config.yaml cookiecutter-pypackage

Or you can set the ``COOKIECUTTER_CONFIG`` environment variable::

    $ export COOKIECUTTER_CONFIG=/home/audreyr/my-custom-config.yaml

If you wish to stick to the built-in config and not load any user config file at all,
use the cli option ``--default-config`` instead. Preventing Cookiecutter from loading
user settings is crucial for writing integration tests in an isolated environment.

Example user config:

.. code-block:: yaml

    default_context:
        full_name: "Audrey Roy"
        email: "audreyr@example.com"
        github_username: "audreyr"
    cookiecutters_dir: "/home/audreyr/my-custom-cookiecutters-dir/"
    replay_dir: "/home/audreyr/my-custom-replay-dir/"
    abbreviations:
        pp: https://github.com/audreyr/cookiecutter-pypackage.git
        gh: https://github.com/{0}.git
        bb: https://bitbucket.org/{0}

Possible settings are:

* default_context: A list of key/value pairs that you want injected as context
  whenever you generate a project with Cookiecutter. These values are treated
  like the defaults in `cookiecutter.json`, upon generation of any project.
* cookiecutters_dir: Directory where your cookiecutters are cloned to when you
  use Cookiecutter with a repo argument.
* replay_dir: Directory where Cookiecutter dumps context data to, which
  you can fetch later on when using the `replay feature`_.
* abbreviations: A list of abbreviations for cookiecutters. Abbreviations can
  be simple aliases for a repo name, or can be used as a prefix, in the form
  `abbr:suffix`. Any suffix will be inserted into the expansion in place of
  the text `{0}`, using standard Python string formatting.  With the above
  aliases, you could use the `cookiecutter-pypackage` template simply by saying
  `cookiecutter pp`, or `cookiecutter gh:audreyr/cookiecutter-pypackage`.
  The `gh` (github) and `bb` (bitbucket) abbreviations shown above are actually
  built in, and can be used without defining them yourself.
