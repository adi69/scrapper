import csv
with open('f1.csv','rb') as f:
    l = list(csv.reader(f))

d={}
for i in l:
    if i[2] in d: print "FUCK!! ", i[2]
    else: d[i[2]] = 1
