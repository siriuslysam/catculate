#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Compute the supply duration for a quantity of food"""

__author__ = "Sam Zhao"
__date__ = "2022-11-14 00:40:39"

import os
import json
import util


macro_file = 'data/macros.csv'
last_line = util.get_last_line(macro_file)
last_line = util.parse_line(last_line)

# Read the regimen info for each cat.
print('Preparing to compute cat macros...')
with open('input/regimen.json') as f:
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
diet_check = all(diet in util.DIETS for diet in diets)
if diet_check is not True:
    raise KeyError('A diet in regimen.json is invalid. The choices are mix, dry, or wet. Verify and try again.')
if len(diets) != 1:
    diet = input('Which diet do you choose: {}? '.format(', '.join('{}'.format(diet) for diet in diets)))
    if diet not in diets:
        raise ValueError('The diet is not listed in regimen.json. The choices are mix, dry, or wet. Verify and try again.')
else:
    diet = diets[0]

# Make some varaibles from regimen dict.
age_group = regimen[name][diet]['age_group']

# Open nutritional facts from inputured food.
if os.path.isfile('foods/'+ regimen[name][diet]['brand'] +'.json'):
    pass
else:
    raise Exception('Food json for {} does not exist'.format(regimen[name][diet]['brand']))
with open('foods/'+ regimen[name][diet]['brand'] +'.json') as f:
    food = json.load(f)

total_weight = food[age_group]['dry']['bag_lbs']
total_weight *= util.LB_TO_KG
desired_dry_kcal_per_cup = float(last_line[-1])
desired_dry_kg_per_cup = desired_dry_kcal_per_cup / food[age_group]['dry']['kcal_per_kg']
dry_total_cups = total_weight / desired_dry_kg_per_cup