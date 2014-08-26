==============
Advanced Usage
==============

Using Pre/Post-Generate Hooks (0.7.0+)
--------------------------------------

You can have Python or Shell scripts that run before and/or after your project
is generated.

Put them in `hooks/` like this::

    cookiecutter-something/
    ├── {{cookiecutter.repo_name}}/
    ├── hooks
    │   ├── pre_gen_project.py
    │   └── post_gen_project.py
    └── cookiecutter.json

Shell scripts work similarly::

    cookiecutter-something/
    ├── {{cookiecutter.repo_name}}/
    ├── hooks
    │   ├── pre_gen_project.sh
    │   └── post_gen_project.sh
    └── cookiecutter.json

It shouldn't be too hard to extend Cookiecutter to work with other types of
scripts too. Pull requests are welcome.

For portability, you should use Python scripts (with extension `.py`) for your
hooks, as these can be run on any platform. However, if you intend for your
template to only be run on a single platform, a shell script (or `.bat` file
on Windows) can be a quicker alternative.

User Config (0.7.0+)
----------------------

If you use Cookiecutter a lot, you'll find it useful to have a
`.cookiecutterrc` file in your home directory like this:

.. code-block:: yaml

    default_context:
        full_name: "Audrey Roy"
        email: "audreyr@gmail.com"
        github_username: "audreyr"
    cookiecutters_dir: "/home/audreyr/my-custom-cookiecutters-dir/"
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
* abbreviations: A list of abbreviations for cookiecutters. Abbreviations can
  be simple aliases for a repo name, or can be used as a prefix, in the form
  `abbr:suffix`. Any suffix will be inserted into the expansion in place of
  the text `{0}`, using standard Python string formatting.  With the above
  aliases, you could use the `cookiecutter-pypackage` template simply by saying
  `cookiecutter pp`, or `cookiecutter gh:audreyr/cookiecutter-pypackage`.
  The `gh` (github) and `bb` (bitbucket) abbreviations shown above are actually
  built in, and can be used without defining them yourself.

Calling Cookiecutter Functions From Python
------------------------------------------

You can use Cookiecutter from Python::

    from cookiecutter.main import cookiecutter

    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')

This is useful if, for example, you're writing a web framework and need to
provide developers with a tool similar to `django-admin.py startproject` or
`npm init`.

See the :ref:`API Reference <apiref>` for more details.


.. _command_line_options:

Command Line Options
--------------------

.. cc-command-line-options::


