#!/usr/bin/env python

import ast

from . import base


class InputPasswordUseLinter(base.BaseLinter):
    """This linter looks for use of the Python "input" function with a string
    argument containing the word "password" in any format.
    """
    off_by_default = False

    _code = 'DUO139'
    _error_tmpl = 'DUO139 avoid using "input" to ask for password, prefer "getpass.getpass"'

    def visit_Call(self, node):
        if getattr(node.func, "id", None) != "input":
            return

        value = self._get_arg_or_kwarg(node)

        if isinstance(value, str) and "password" in value.lower():
            self.results.append(
                base.Flake8Result(
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    message=self._error_tmpl
                )
            )

    def _get_arg_or_kwarg(self, node):
        if node.args:
            arg = node.args[0]
            if isinstance(arg, ast.Constant):
                return arg.value
        if node.keywords:
            value = node.keywords[0].value
            if isinstance(value, ast.Constant):
                return value.value
        return None
