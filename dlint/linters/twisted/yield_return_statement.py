#!/usr/bin/env python

from .. import base


class YieldReturnStatementLinter(base.BaseLinter):
    """This linter looks for inlineCallbacks functions that have
    non-empty return statements. Using a non-empty return statement and a
    yield statement in the same function is a syntax error.
    """
    off_by_default = False

    _code = 'DUO101'
    _error_tmpl = 'DUO101 "inlineCallbacks" function cannot have non-empty "return" statement'

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
