#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Compute the daily macros for a cat."""

__author__ = "Sam Zhao"
__date__ = "2022-07-30 01:47:35"

import json

with open('config/regimen.json') as f:
    regimen = json.load(f)


print(regimen)