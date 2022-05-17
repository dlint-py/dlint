#!/usr/bin/env python

import unittest

import dlint


class TestBadPycryptoUse(dlint.test.base.BaseTest):

    def test_bad_pycrypto_usage(self):
        python_node = self.get_ast_node(
            """
            import Crypto
            """
        )

        linter = dlint.linters.BadPycryptoUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=2,
                col_offset=0,
                message=dlint.linters.BadPycryptoUseLinter._error_tmpl
            )
        ]

        assert result == expected

    def test_bad_pycrypto_from_usage(self):
        python_node = self.get_ast_node(
            """
            from Crypto import AES
            """
        )

        linter = dlint.linters.BadPycryptoUseLinter()
        linter.visit(python_node)

        result = linter.get_results()
        expected = [
            dlint.linters.base.Flake8Result(
                lineno=2,
                col_offset=0,
                message=dlint.linters.BadPycryptoUseLinter._error_tmpl
            )
        ]

        assert result == expected


if __name__ == "__main__":
    unittest.main()
