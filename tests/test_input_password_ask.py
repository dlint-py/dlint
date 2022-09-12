#!/usr/bin/env python

import unittest

import dlint


class TestInputPasswordUse(dlint.test.base.BaseTest):

    def test_no_password(self):
        python_node = self.get_ast_node(
            """
            input("enter your name:")
            """
        )

        linter = dlint.linters.InputPasswordUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = []

        assert result == expected

    def test_input_asks_password(self):
        python_node = self.get_ast_node(
            """
            input("enter your password:")
            """
        )

        linter = dlint.linters.InputPasswordUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=2,
                col_offset=0,
                message=dlint.linters.InputPasswordUseLinter._error_tmpl
            )
        ]

        assert result == expected


if __name__ == "__main__":
    unittest.main()
