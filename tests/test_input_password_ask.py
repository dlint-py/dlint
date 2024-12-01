#!/usr/bin/env python

import pytest
import unittest

import dlint


@pytest.mark.parametrize("code", [
    """input('enter your name:')""",
    """input = 1""",
    """password = 'something'""",
])
def test_input_password_not_used(code):
    python_node = dlint.test.base.get_ast_node(code)

    linter = dlint.linters.InputPasswordUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = []

    assert result == expected


@pytest.mark.parametrize("code", [
    """input('enter your password:')""",
    """input('enter your PASSWORD:')""",
    # unable to detect if the intent wasn't to ask for password because word 'password' is present
    """input('Please enter your name. Please do not enter your password')""",
    """input(prompt='enter your PASSWORD:')""",
])
def test_input_password_bad(code):
    python_node = dlint.test.base.get_ast_node(code)

    linter = dlint.linters.InputPasswordUseLinter()
    linter.visit(python_node)

    result = linter.get_results()

    expected = [
        dlint.linters.base.Flake8Result(
            lineno=1,
            col_offset=0,
            message=dlint.linters.InputPasswordUseLinter._error_tmpl
        )
    ]

    assert result == expected


if __name__ == "__main__":
    unittest.main()
