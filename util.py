#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility functions and definitions."""

__author__ = "Sam Zhao"
__date__ = "2022-08-05 02:11:36"

import os


TERMINATORS = ['\r', '\n']
LB_TO_KG = 0.45359237
DIETS = ['mix','dry','wet']
SMALLEST_CUP = 0.0625

def round_nearest(x, a):
    """Round the number to the nearest desired interval.
    
    :param x: Number to be be rounded.
    :type x: int, float
    :param a: Interval to be rounded to.
    :type a: int, float
    :return: Rounded number.
    :rtype: int, float
    """
    return round(x / a) * a

def add_s(num):
    """Output a plural 's' if the value is more than 1.

    :param num: Number to be checked.
    :type num: int, float
    :return: string of s and nothing.
    :rtype: str
    """
    if num > 1:
        return 's'
    else:
        return ''

def get_last_line(file):
    """Get the last line of a file like csv.

    :param file: Filename to find last line.
    :type file: str
    :return: Last line.
    :rtype: str
    """
    with open(file, 'rb') as file:
        # Try to catch if the file is a one-liner.
        try:
            # Go to the end of the file before the last breakline.
            file.seek(-2, os.SEEK_END) 
            # Keep reading backwards until you find the next breakline.
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR) 
        except OSError:
            file.seek(0)
        return file.readline().decode()

def delete_tails(string):
    """Delete line terminators from data files.

    :param string: String to be parsed.
    :type string: str
    :return: New string without line terminators
    :rtype: str
    
    """
    for tail in TERMINATORS:
        string = string.replace(tail,'')
    return string

def parse_line(string):
    return [delete_tails(elem) for elem in string.split(',')]