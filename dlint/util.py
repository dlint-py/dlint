#!/usr/bin/env python

def lstartswith(l1, l2):
    if len(l2) > len(l1):
        return False
    return l1[:len(l2)] == l2


def lendswith(l1, l2):
    if len(l2) > len(l1):
        return False
    return l1[len(l1) - len(l2):] == l2
