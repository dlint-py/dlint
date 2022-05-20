#!/usr/bin/env python

import unittest

import dlint


class TestUtil(unittest.TestCase):

    def test_abc(self):
        assert dlint.util.ABC


if __name__ == "__main__":
    unittest.main()
