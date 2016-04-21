'''
import csv
with open(sys.argv[1], 'rb') as f:
    reader = csv.reader(f)
    L = list(reader)

for i in L:
    i[2].strip()
'''

