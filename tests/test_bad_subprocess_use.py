#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

import dlint


class TestBadSubprocessUse(dlint.test.base.BaseTest):

    def test_bad_subprocess_usage(self):
        python_node = self.get_ast_node(
            """
            import subprocess

            command = "/bin/echo"

            subprocess.call(shell=True)
            subprocess.check_call(shell=True)
            subprocess.check_output(shell=True)
            subprocess.Popen(shell=True)
            subprocess.run(shell=True)
            subprocess.run(command,shell=True)
            """
        )

        linter = dlint.linters.BadSubprocessUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=6,
                col_offset=0,
                message=dlint.linters.BadSubprocessUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=7,
                col_offset=0,
                message=dlint.linters.BadSubprocessUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=8,
                col_offset=0,
                message=dlint.linters.BadSubprocessUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=9,
                col_offset=0,
                message=dlint.linters.BadSubprocessUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=10,
                col_offset=0,
                message=dlint.linters.BadSubprocessUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=11,
                col_offset=0,
                message=dlint.linters.BadSubprocessUseLinter._error_tmpl
            ),
        ]

        assert result == expected

    def test_subprocess_usage(self):
        python_node = self.get_ast_node(
            """
            import subprocess

            command = "/bin/echo"

            subprocess.call(command)
            subprocess.call(shell=False)
            subprocess.check_call(shell=False)
            subprocess.check_output(shell=False)
            subprocess.Popen(shell=False)
            subprocess.run(command)
            subprocess.run(shell=False)
            """
        )

        linter = dlint.linters.BadSubprocessUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = []

        assert result == expected


if __name__ == "__main__":
    unittest.main()
