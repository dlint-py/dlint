#!/usr/bin/env python

import unittest

import dlint


class TestBadCompileUse(dlint.test.base.BaseTest):

    def test_bad_compile_usage(self):
        python_node = self.get_ast_node(
            """
            var = 1

            result = compile('var + 1', '<string>', 'eval')
            """
        )

        linter = dlint.linters.BadCompileUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=4,
                col_offset=9,
                message=dlint.linters.BadCompileUseLinter._error_tmpl
            )
        ]

        assert result == expected


if __name__ == "__main__":
    unittest.main()
