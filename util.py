#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility functions and definitions."""

__author__ = "Sam Zhao"
__date__ = "2022-08-05 02:11:36"


def round_nearest(x, a):
    """Round the number to the nearest desired number.
    
    """
    return round(x / a) * a

def add_s(num):
    """Output a plural 's' if the value is more than 1.

    """
    if num > 1:
        return 's'
    else:
        return ''