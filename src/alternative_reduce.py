#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--keys', nargs='+', required=True)   # hashtags
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# always use src/outputs relative to this script
OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

# 2020 is a leap year
month_days = [31,29,31,30,31,30,31,31,30,31,30,31]

def doy_from_filename(fname):
    # expects: geoTwitter20-MM-DD.zip.lang
    # split off extension(s)
    stem = fname.split('.zip')[0]          # geoTwitter20-MM-DD
    date_part = stem.replace('geoTwitter', '')  # 20-MM-DD
    yy, mm, dd = date_part.split('-')      # ['20','MM','DD']
    mm = int(mm); dd = int(dd)

    month_days = [31,29,31,30,31,30,31,31,30,31,30,31]
    return sum(month_days[:mm-1]) + dd

# index files by day-of-year
day_to_path = {}
for fname in os.listdir(OUTPUTS_DIR):
    if fname.endswith('.zip.lang'):
        day_to_path.setdefault(doy_from_filename(fname), os.path.join(OUTPUTS_DIR, fname))

# build series: series[key][doy] = total hashtag count that day
series = defaultdict(dict)
days = list(range(1, 367))

for key in args.keys:
    for doy in days:
        path = day_to_path.get(doy)
        if path is None:
            series[key][doy] = 0
            continue
        with open(path) as f:
            data = json.load(f)
        series[key][doy] = sum(data.get(key, {}).values())

# tiny sanity print so you can trust it’s reading the full year
print('loaded days:', len(day_to_path), 'example day 153 (# June 1):',
      {k: series[k].get(153, 0) for k in args.keys})

# plot
plt.figure(figsize=(14,8))
for key in args.keys:
    plt.plot(days, [series[key][d] for d in days], label=key, linewidth=1.5)

plt.xlabel('Day of Year (2020)')
plt.ylabel('Tweet Count')
plt.title('Tweet Counts by Hashtag(s) Over Time')
plt.legend()
plt.tight_layout()
plt.savefig('alternative_reduce.png', dpi=200)
plt.close()
print('alternative_reduce.png')
