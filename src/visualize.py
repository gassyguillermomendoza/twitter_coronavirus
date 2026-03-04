#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

import matplotlib
matplotlib.use('Agg')  # needed on lambda server
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in list(counts[args.key].keys()):
        denom = counts['_all'].get(k, 0)
        if denom != 0:
            counts[args.key][k] /= denom
        else:
            # avoid divide-by-zero / missing keys
            del counts[args.key][k]

# sort items by value (high->low) and take top 10
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)[:10]

# final results should be sorted from low to high
items = sorted(items, key=lambda item: (item[1],item[0]))

# make bar chart
keys = [k for k,v in items]
vals = [v for k,v in items]

plt.figure(figsize=(10,5))
plt.bar(keys, vals)
plt.xticks(rotation=45, ha='right')
plt.xlabel('key')
plt.ylabel('percent' if args.percent else 'count')
plt.title(args.key)
plt.tight_layout()

# save to png (name based on input + key)
base = os.path.splitext(os.path.basename(args.input_path))[0]
safe_key = args.key.replace('#','').replace('/','_').replace(' ','_')
out_path = f'{base}.{safe_key}' + ('.percent.png' if args.percent else '.png')

plt.savefig(out_path, dpi=200)
print(out_path)
