#!/usr/bin/env python

import ast
import textwrap
import unittest


def get_ast_node(s):
    return ast.parse(textwrap.dedent(s))


class BaseTest(unittest.TestCase):

    @staticmethod
    def get_ast_node(s):
        return get_ast_node(s)
