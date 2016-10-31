#!/usr/bin/env python3
import subprocess
from datetime import datetime, timedelta
import sys

p = subprocess.Popen(['journalctl', '--since', 'today', '-o', 'short-iso'], stdout=subprocess.PIPE)

dates = []

next(p.stdout)

for line in p.stdout:
    line = line.decode()
    line = line[:24]
    try:
        date = datetime.strptime(line, "%Y-%m-%dT%H:%M:%S%z" )
    except ValueError:
        continue
    dates.append(date)

pairs = zip(dates, dates[1:])

fmt = "%H:%M:%S"

print("start:  {}".format(dates[0].strftime(fmt)))

delta = 10
if len(sys.argv) > 1:
    delta = int(sys.argv[1])

for pair in pairs:
    if pair[1] - pair[0] > timedelta(minutes=delta):
        time0 = pair[0].strftime(fmt)
        time1 = pair[1].strftime(fmt)
        print("pause:  {} - {}".format(time0, time1))

print("end:    {}".format(dates[-1].strftime(fmt)))
