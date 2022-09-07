#!/usr/bin/env python

from .helpers import bad_builtin_use


class BadExecUseLinter(bad_builtin_use.BadBuiltinUseLinter):
    """This linter looks for use of the Python "exec" function. This function
    makes it far too easy to achieve arbitrary code execution, so we shouldn't
    support it in any context.
    """
    off_by_default = False

    _code = 'DUO105'
    _error_tmpl = 'DUO105 use of "exec" is insecure'

    @property
    def illegal_builtin(self):
        return 'exec'
