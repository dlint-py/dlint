#!/usr/bin/env python

import unittest

import dlint


class TestBadDlUse(dlint.test.base.BaseTest):

    def test_bad_dl_usage(self):
        python_node = self.get_ast_node(
            """
            import dl
            """
        )

        linter = dlint.linters.BadDlUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=2,
                col_offset=0,
                message=dlint.linters.BadDlUseLinter._error_tmpl
            )
        ]

        assert result == expected


if __name__ == "__main__":
    unittest.main()
