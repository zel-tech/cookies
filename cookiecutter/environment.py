# -*- coding: utf-8 -*-

from jinja2 import Environment, StrictUndefined

from .exceptions import UnknownExtension


class ExtensionLoaderMixin(object):
    """Mixin that provides a sane way of loading extensions specified in a
    given context.

    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    """
    def __init__(self, **kwargs):
        context = kwargs.pop('context', {})

        try:
            super(ExtensionLoaderMixin, self).__init__(
                extensions=self._read_extensions(context),
                **kwargs
            )
        except ImportError as err:
            raise UnknownExtension('Unable to load extension: {}'.format(err))

    def _read_extensions(self, context):
        """Return a list of extensions as str to be passed on to the jinja2
        env. If context does not contain the relevant info, return an empty
        list instead.
        """
        try:
            extensions = context['cookiecutter']['_extensions']
        except KeyError:
            return []
        else:
            return [str(ext) for ext in extensions]


class StrictEnvironment(ExtensionLoaderMixin, Environment):
    """Jinja2 environment that raises an error when it hits a variable
    which is not defined in the context used to render a template.
    """
    def __init__(self, **kwargs):
        super(StrictEnvironment, self).__init__(
            undefined=StrictUndefined,
            **kwargs
        )
