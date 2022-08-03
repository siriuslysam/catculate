#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Compute the daily macros for a cat."""

__author__ = "Sam Zhao"
__date__ = "2022-07-30 01:47:35"

import json


list_diets = ['mix','dry','wet']

# Read the regimen info for each cat.
print('Preparing to compute cat macros...')
with open('config/regimen.json') as f:
    regimen = json.load(f)

# Ask for which cat to calculate macros for.
cats = list(regimen.keys())
if len(cats) != 1:
    name = input('Which cat do you choose: {}? '.format(', '.join('{}'.format(cat) for cat in cats)))
    if name not in cats:
        raise ValueError('The name of the cat is not listed in regimen.json. Verify and try again.')
else:
    name = cats[0]

# Check if regimen contains a valid diet.
# Then ask for which diet type to choose: mix, dry, or wet.
diets = list(regimen[name].keys())
diet_check = all(diet in list_diets for diet in diets)
if diet_check is not True:
    raise KeyError('A diet in regimen.json is invalid. The choices are mix, dry, or wet. Verify and try again.')
if len(diets) != 1:
    diet = input('Which diet do you choose: {}? '.format(', '.join('{}'.format(diet) for diet in diets)))
    if diet not in diets:
        raise ValueError('The diet is not listed in regimen.json. The choices are mix, dry, or wet. Verify and try again.')
else:
    diet = diets[0]



print(regimen['Daikon'])