#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import sys
import unittest

import pytest

import dlint

IS_PYTHON_3_7 = sys.version_info >= (3, 7)

ILLEGAL_MODULE_ATTRIBUTES = [
    (module_path, attribute)
    for module_path, attributes in dlint.linters.BadReCatastrophicUseLinter().illegal_module_attributes.items()
    for attribute in attributes
]


@pytest.mark.parametrize("module_path, attribute", ILLEGAL_MODULE_ATTRIBUTES)
def test_bad_re_catastrophic_usage(module_path, attribute):
    python_node = dlint.test.base.get_ast_node(
        """
        import {MODULE_PATH}

        {MODULE_PATH}.{ATTRIBUTE}('(a+)+z')
        """.format(MODULE_PATH=module_path, ATTRIBUTE=attribute)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = [
        dlint.linters.base.Flake8Result(
            lineno=4,
            col_offset=0,
            message=dlint.linters.BadReCatastrophicUseLinter._error_tmpl
        ),
    ]

    assert result == expected


@pytest.mark.parametrize("module_path, attribute", ILLEGAL_MODULE_ATTRIBUTES)
def test_bad_re_catastrophic_usage_from_import(module_path, attribute):
    python_node = dlint.test.base.get_ast_node(
        """
        from {MODULE_PATH} import {ATTRIBUTE}

        {ATTRIBUTE}('(a+)+z')
        """.format(MODULE_PATH=module_path, ATTRIBUTE=attribute)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = [
        dlint.linters.base.Flake8Result(
            lineno=4,
            col_offset=0,
            message=dlint.linters.BadReCatastrophicUseLinter._error_tmpl
        ),
    ]

    assert result == expected


LARGE_QUANTIFIERS = [
    "+", "+?",
    "*", "*?",
    "{1,10}", "{1,10}?",
    "{10}", "{10}?",
    "{,10}", "{,10}?",
    "{10,}", "{10,}?",
]
SMALL_QUANTIFIERS = [
    "?", "??",
    "{1,9}", "{1,9}?",
    "{9}", "{9}?",
    "{,9}", "{,9}?",
]


@pytest.mark.parametrize("quantifier1", LARGE_QUANTIFIERS)
@pytest.mark.parametrize("quantifier2", LARGE_QUANTIFIERS)
def test_bad_re_nested_large_quantifiers(quantifier1, quantifier2):
    python_node = dlint.test.base.get_ast_node(
        """
        import re

        re.search('(a{QUANTIFIER1}){QUANTIFIER2}z')
        """.format(QUANTIFIER1=quantifier1, QUANTIFIER2=quantifier2)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = [
        dlint.linters.base.Flake8Result(
            lineno=4,
            col_offset=0,
            message=dlint.linters.BadReCatastrophicUseLinter._error_tmpl
        ),
    ]

    assert result == expected


@pytest.mark.parametrize("quantifier1", LARGE_QUANTIFIERS)
@pytest.mark.parametrize("quantifier2", SMALL_QUANTIFIERS)
def test_bad_re_nested_small_quantifiers(quantifier1, quantifier2):
    python_node = dlint.test.base.get_ast_node(
        """
        import re

        re.search('(a{QUANTIFIER1}){QUANTIFIER2}z')
        """.format(QUANTIFIER1=quantifier1, QUANTIFIER2=quantifier2)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = []

    assert result == expected


OVERLAPPING_ALTERNATIONS = [
    (r".|[a-c]", True),  # anything and range
    (r"[^d]|[a-c]", True),  # not literal and range
    (r"[^b]|[a-c]", True),  # not literal partial and range
    (r"[^d]|[^b]|[a-c]", True),  # multiple not literal and range
    (r"[^abcAB]|[a-c]|[A-C]", True),  # negate literal and multiple range
    (r"\\d|123", True),  # digit category and multiple digit
    (r"\\w|abc", True),  # word category and multiple letter
    (r"\\s|   ", True),  # whitespace category and multiple space
    (r"[^\\W]|[a-c]", True),  # negate not word and range
    (r"d|[a-c]", False),  # literal and range
    (r"[^a]|a", False),  # not literal and literal
    (r"[^abcABC]|[a-c]|[A-C]", False),  # negate literal and multiple range
    (r"[a-c]|[d-f]", False),  # range and range
    (r"[abc]|[d-f]", False),  # literals and range
    (r"[a-c]|[^a-c]", False),  # range and negate range
]


@pytest.mark.parametrize("alternation, overlapping", OVERLAPPING_ALTERNATIONS)
def test_bad_re_catastrophic_nested_quantifier_alternation(alternation, overlapping):
    python_node = dlint.test.base.get_ast_node(
        """
        import re

        re.search('({ALTERNATION})+z')
        """.format(ALTERNATION=alternation)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = [] if not overlapping else [
        dlint.linters.base.Flake8Result(
            lineno=4,
            col_offset=0,
            message=dlint.linters.BadReCatastrophicUseLinter._error_tmpl
        )
    ]

    assert result == expected


@pytest.mark.parametrize("quantifier", SMALL_QUANTIFIERS)
def test_bad_re_catastrophic_nested_small_quantifier_alternation(quantifier):
    python_node = dlint.test.base.get_ast_node(
        """
        import re

        re.search('(a|a){QUANTIFIER}z')
        """.format(QUANTIFIER=quantifier)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = []

    assert result == expected


# sre_parse optimization nullifies this alternation check in Python 3.7+
OVERLAPPING_ALTERNATIONS_PY_3_7 = [
    (r"a|[a-c]", True),  # literal and range
    (r"[a-c]|[c-e]", True),  # range and range
    (r"\\w|[a-c]", True),  # word and range
    (r"\\S|[a-c]", True),  # not whitespace and range
    (r"\\d|1", True),  # digit category and digit
    (r"\\w|a", True),  # word category and letter
    (r"\\s| ", True),  # whitespace category and space
]


@pytest.mark.parametrize("alternation, overlapping", OVERLAPPING_ALTERNATIONS_PY_3_7)
def test_bad_re_catastrophic_nested_quantifier_alternation_py_3_7(alternation, overlapping):
    python_node = dlint.test.base.get_ast_node(
        """
        import re

        re.search('({ALTERNATION})+z')
        """.format(ALTERNATION=alternation)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()

    expected = [] if IS_PYTHON_3_7 or not overlapping else [
        dlint.linters.base.Flake8Result(
            lineno=4,
            col_offset=0,
            message=dlint.linters.BadReCatastrophicUseLinter._error_tmpl
        )
    ]

    assert result == expected


OK_RE_CALLS = [
    r"re.search('[abc]+[def]*')",  # adjacent quantifier ok
    r"re.search('[abc]+([def]*)')",  # diagonal quantifier ok
    r"re.search('(?P<name>[foo])(?(name)yes|no)')",  # groupref ok
    r"re.search(s)",  # variable argument ok, or at least don't explode
    r"re.search()",  # missing argument ok, or at least don't explode
    r"re.search('(foo')",  # malformed expression ok, or at least don't explode
    r"re.purge()",  # legal attribute ok
]


@pytest.mark.parametrize("re_call", OK_RE_CALLS)
def test_bad_re_catastrophic_not_literal_string(re_call):
    python_node = dlint.test.base.get_ast_node(
        """
        import re

        s = 'test'

        {RE_CALL}
        """.format(RE_CALL=re_call)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = []

    assert result == expected


BACKTRACKABLE = [
    (r"(a+)+z", True),  # present subsequent subexpression
    (r"(abc|[a-c])+z", True),  # alternation present subsequent subexpression
    (r"(a+)+", False),  # missing subsequent subexpression
    (r"(a+)+x?y?z?", False),  # all subsequent are optional
    (r"(a+)+z{0,5}", False),  # all subsequent are optional
    (r"(a+)+z{,5}", False),  # all subsequent are optional
    (r"(a+)+z*", False),  # all subsequent are optional
    (r"(a+)+b*c?d*?e", True),  # long propagation
    (r"(a+)+$", True),  # at end propagation
    (r"(a+)+\\Z", True),  # at end string propagation
    (r"(a|(bc|[b-c]))+z", True),  # parent subsequent subexpression
    (r"(a|(bc|[b-c])+z)", True),  # sibling subsequent subexpression
    (r"(a|(bc|[b-c]z)+)", False),  # sibling expression parent quantifier
    (r"(?://[^\n]*)*", False),  # found in the wild
    (r"(?:[ \t].*?(?:\n|$))*", False),  # found in the wild
    (r"<.*?>|((?:\\w[-\\w]*|&.*?;)+)", False),  # found in the wild
    (r"^(\\s+)\\w+=.*(\\n\\1\\w+=.*)+", False),  # found in the wild
    (r"([^*{}\\s]@|[^*{}@]|\\*(?!/))+", False),  # found in the wild
]


@pytest.mark.parametrize("expression, catastrophic", BACKTRACKABLE)
def test_bad_re_catastrophic_backtrackable(expression, catastrophic):
    python_node = dlint.test.base.get_ast_node(
        """
        import re

        re.search('{EXPRESSION}')
        """.format(EXPRESSION=expression)
    )

    linter = dlint.linters.BadReCatastrophicUseLinter()
    linter.visit(python_node)

    result = linter.get_results()
    expected = [] if not catastrophic else [
        dlint.linters.base.Flake8Result(
            lineno=4,
            col_offset=0,
            message=dlint.linters.BadReCatastrophicUseLinter._error_tmpl
        )
    ]

    assert result == expected


if __name__ == "__main__":
    unittest.main()
