#!/usr/bin/env python

import abc
import sys

if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta(str('ABC'), (), {})


def lstartswith(l1, l2):
    if len(l2) > len(l1):
        return False
    return l1[:len(l2)] == l2


def lendswith(l1, l2):
    if len(l2) > len(l1):
        return False
    return l1[len(l1) - len(l2):] == l2
