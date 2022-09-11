#!/usr/bin/env python

import unittest

import dlint


class TestUtil(unittest.TestCase):

    def test_lendswith(self):
        assert not dlint.util.lendswith([1, 2], [1, 2, 3])
        assert not dlint.util.lendswith([1, 2, 3], [1, 2])

        assert dlint.util.lendswith([1, 2, 3], [2, 3])


if __name__ == "__main__":
    unittest.main()
