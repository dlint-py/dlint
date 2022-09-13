#!/usr/bin/env python

from . import base


class BadInputUseLinter(base.BaseLinter):
    """This linter looks for use of the Python "input" function.
    In Python 3 raw_input() functionality has been moved to input().
    """
    off_by_default = False

    _code = 'DUO108'
    _error_tmpl = 'DUO108 use of "input" is insecure'

    def __init__(self, *args, **kwargs):
        self.unsafe_input_import = True

        super(BadInputUseLinter, self).__init__(*args, **kwargs)

    def visit_ImportFrom(self, node):
        # Using input from six.moves is valid, so if input is imported
        # in a safe way, allow input to be used for the rest of the file
        if (node.module == 'six.moves'
                and any(alias.name == 'input' for alias in node.names)):
            self.unsafe_input_import = False
