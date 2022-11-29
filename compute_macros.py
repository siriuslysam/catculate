#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Compute the daily macros for a cat."""

__author__ = "Sam Zhao"
__date__ = "2022-07-30 01:47:35"

import os
import json
import csv
from datetime import date
from fractions import Fraction
import util


header = ['Date', 'Total Food (kcal)', 'Wet Food (kcal)', 'Dry Food (kcal)']

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
wet_portion = regimen[name][diet]['wet_portion']
dry_portion = regimen[name][diet]['dry_portion']
kcal_min = regimen[name][diet]['kcal_min']
kcal_max = regimen[name][diet]['kcal_max']

# Switch case to compute macros for specific diet.
if diet == 'mix':
    # Open nutritional facts from inputured food.
    if os.path.isfile('foods/'+ regimen[name][diet]['brand'] +'.json'):
        pass
    else:
        raise Exception('Food json for {} does not exist'.format(regimen[name][diet]['brand']))
    with open('foods/'+ regimen[name][diet]['brand'] +'.json') as f:
        food = json.load(f)

    # Compute wet food potion.
    wet_kcal = food[age_group]['wet']['kcal']
    if wet_portion == 'half_can':
        wet_kcal /= 2.0
        wet_can = 0.5
    elif wet_portion == 'full_can':
        wet_can = 1.0

    # Compute dry food portion by finding the range of calories.
    dry_kcal_per_cup = food[age_group]['dry']['kcal_per_cup']
    if dry_portion == 'remaining':
        dry_cup_min = (kcal_min - wet_kcal) / dry_kcal_per_cup
        dry_cup_max = (kcal_max - wet_kcal) / dry_kcal_per_cup

        # Choose the closest quarter-cup portion.
        dry_cup_min_near = util.round_nearest(dry_cup_min, 0.25)
        dry_cup_max_near = util.round_nearest(dry_cup_max, 0.25)

        dry_cup_min_err = abs(dry_cup_min_near - dry_cup_min)
        dry_cup_max_err = abs(dry_cup_max_near - dry_cup_max)

        if dry_cup_max_err < dry_cup_min_err:
            dry_cup = dry_cup_max_near
        else:
            dry_cup = dry_cup_min_near

    dry_kcal = dry_cup * dry_kcal_per_cup
    total_kcal = wet_kcal + dry_kcal
elif diet == 'wet':
    pass
elif diet == 'dry':
    pass

# Print computed macros.
print("\n***** {}'s Daily Macros *****".format(name))
print('- Total Feeding')
if diet in ['mix','wet']:
    print('Wet food: {} can{}'.format((Fraction(wet_can)),util.add_s(wet_can)))
if diet in ['mix','dry']:
    print('Dry food: {} cup{}'.format(str(Fraction(dry_cup)),util.add_s(dry_cup)))

print('\n- Suggested Meals')
if diet == 'mix':
    print('Breakfast: {} cup{}'.format(str(Fraction(dry_cup/2.0)),util.add_s(dry_cup/2.0)))
    print('Dinner: {} can{}'.format((Fraction(wet_can)),util.add_s(wet_can)))
    print('Midnight: {} cup{}'.format(str(Fraction(dry_cup/2.0)),util.add_s(dry_cup/2.0)))
elif diet == 'wet':
    print('Breakfast: {} can{}'.format((Fraction(wet_can/3.0)),util.add_s(wet_can/3.0)))
    print('Dinner: {} can{}'.format((Fraction(wet_can/3.0)),util.add_s(wet_can/3.0)))
    print('Midnight: {} can{}'.format((Fraction(wet_can/3.0)),util.add_s(wet_can/3.0)))
elif diet == 'dry':
    print('Breakfast: {} cup{}'.format((Fraction(dry_cup/3.0)),util.add_s(dry_cup/3.0)))
    print('Dinner: {} cup{}'.format((Fraction(dry_cup/3.0)),util.add_s(dry_cup/3.0)))
    print('Midnight: {} cup{}'.format((Fraction(dry_cup/3.0)),util.add_s(dry_cup/3.0)))

# Create the data csv if it doesn't exist.
macro_file = 'data/macros.csv'
if not os.path.isdir('data'):
    os.mkdir('data')
if not os.path.isfile(macro_file):
    with open(macro_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# Log the data, but skip if it's the same as the last entry.
last_line = util.get_last_line(macro_file)
with open(macro_file, 'a', newline='') as f:
    writer = csv.writer(f)
    data = [total_kcal, wet_kcal, dry_kcal]
    if [util.delete_tails(elem) for elem in last_line.split(',')] == header:
        today = date.today()
        data.insert(0,today.strftime("%Y-%m-%d"))
        writer.writerow(data)
    else:
        last_data = [float(util.delete_tails(elem)) for elem in last_line.split(',')[1:]]
        if data != last_data:
            today = date.today()
            data.insert(0,today.strftime("%Y-%m-%d"))
            writer.writerow(data)