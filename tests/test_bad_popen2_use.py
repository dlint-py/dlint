#!/usr/bin/env python

import unittest

import dlint


class TestBadPopen2Use(dlint.test.base.BaseTest):

    def test_bad_popen2_usage(self):
        python_node = self.get_ast_node(
            """
            import popen2
            """
        )

        linter = dlint.linters.BadPopen2UseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=2,
                col_offset=0,
                message=dlint.linters.BadPopen2UseLinter._error_tmpl
            )
        ]

        assert result == expected


if __name__ == "__main__":
    unittest.main()
