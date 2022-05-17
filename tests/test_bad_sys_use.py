#!/usr/bin/env python

import unittest

import dlint


class TestBadSysUse(dlint.test.base.BaseTest):

    def test_bad_sys_usage(self):
        python_node = self.get_ast_node(
            """
            import sys

            sys.call_tracing(lambda: 42, ())
            sys.setprofile(lambda: 42)
            sys.settrace(lambda: 42)
            """
        )

        linter = dlint.linters.BadSysUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=4,
                col_offset=0,
                message=dlint.linters.BadSysUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=5,
                col_offset=0,
                message=dlint.linters.BadSysUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=6,
                col_offset=0,
                message=dlint.linters.BadSysUseLinter._error_tmpl
            ),
        ]

        assert result == expected


if __name__ == "__main__":
    unittest.main()
