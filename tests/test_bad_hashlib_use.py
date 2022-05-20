#!/usr/bin/env python

import unittest

import dlint


class TestBadHashlibUse(dlint.test.base.BaseTest):

    def test_bad_hashlib_usage(self):
        python_node = self.get_ast_node(
            """
            import hashlib

            var = 'echo "TEST"'

            m1 = hashlib.md5()
            m2 = hashlib.sha1()
            """
        )

        linter = dlint.linters.BadHashlibUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=6,
                col_offset=5,
                message=dlint.linters.BadHashlibUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=7,
                col_offset=5,
                message=dlint.linters.BadHashlibUseLinter._error_tmpl
            ),
        ]

        assert result == expected

    def test_hashlib_used_for_security(self):
        python_node = self.get_ast_node(
            """
            import hashlib

            var = 'echo "TEST"'

            m1 = hashlib.md5(usedforsecurity=True)
            m2 = hashlib.sha1(usedforsecurity=True)
            """
        )

        linter = dlint.linters.BadHashlibUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=6,
                col_offset=5,
                message=dlint.linters.BadHashlibUseLinter._error_tmpl
            ),
            dlint.linters.base.Flake8Result(
                lineno=7,
                col_offset=5,
                message=dlint.linters.BadHashlibUseLinter._error_tmpl
            ),
        ]

        assert result == expected

    def test_hashlib_not_used_for_security(self):
        python_node = self.get_ast_node(
            """
            import hashlib

            var = 'echo "TEST"'

            m1 = hashlib.md5(usedforsecurity=False)
            m2 = hashlib.sha1(usedforsecurity=False)
            """
        )

        linter = dlint.linters.BadHashlibUseLinter()
        linter.visit(python_node)

        result = linter.get_results()

        assert len(result) == 0


if __name__ == "__main__":
    unittest.main()
