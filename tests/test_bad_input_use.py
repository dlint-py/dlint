#!/usr/bin/env python

import unittest

import dlint


class TestBadInputUse(dlint.test.base.BaseTest):

    def test_empty(self):
        python_node = self.get_ast_node(
            """
            """
        )

        linter = dlint.linters.BadInputUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = []

        assert result == expected

    def test_bad_input_usage(self):
        python_node = self.get_ast_node(
            """
            var = 1

            result = input('var + 1')
            """
        )

        linter = dlint.linters.BadInputUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = []

        assert result == expected

    def test_six_moves_input_usage(self):
        python_node = self.get_ast_node(
            """
            from six.moves import input

            var = 1

            result = input('var + 1')
            """
        )

        linter = dlint.linters.BadInputUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = []

        assert result == expected

    def test_no_input_usage(self):
        python_node = self.get_ast_node(
            """
            import os

            var = 'test'

            os.path.join(var)
            """
        )

        linter = dlint.linters.BadInputUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = []

        assert result == expected

    def test_bad_input_variable_usage(self):
        python_node = self.get_ast_node(
            """
            input = 1
            """
        )

        linter = dlint.linters.BadInputUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = []

        assert result == expected


if __name__ == "__main__":
    unittest.main()
