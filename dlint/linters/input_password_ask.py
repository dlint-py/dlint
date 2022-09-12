#!/usr/bin/env python

from . import base


class InputPasswordUseLinter(base.BaseLinter):
    """This linter looks for use of the Python "input" function with a string
    argument containing the word "password" in any format.
    """
    off_by_default = False

    _code = 'DUO139'
    _error_tmpl = 'DUO139 avoid using "input" to ask for password'

    def visit_Call(self, node):

        if (node.func.id == "input"):
            value = self._get_arg_or_kwarg(node)

            if "password" in value.lower():
                self.results.append(
                    base.Flake8Result(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        message=self._error_tmpl
                    )
                )

    def _get_arg_or_kwarg(self, node):
        if node.args:
            return node.args[0].value
        if node.keywords:
            return node.args[0].value
