# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 21:44:53 2023

@author: chrischris
"""

import csv

file_name = 'L10I05D1K'
lines = []

with open('./'+file_name+'.data', 'r') as f:
    for row in f:
        line = row.strip().split(' ')[3:]
        lines.append(', '.join(line))
        
with open('./'+file_name+'.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows([[item] for item in lines])