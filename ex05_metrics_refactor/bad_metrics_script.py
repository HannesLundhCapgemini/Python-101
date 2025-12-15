# BAD EXAMPLE - TO BE REFACTORED

import json
import os
import time

data_file = "metrics.json"

if not os.path.exists(data_file):
    print("no metrics file!")
    exit(1)

f = open(data_file)
raw = json.load(f)
f.close()

values = []
for r in raw:
    values.append(r["value"])

s = 0
for v in values:
    s += v

avg = s / len(values)
print("avg is " + str(avg))
