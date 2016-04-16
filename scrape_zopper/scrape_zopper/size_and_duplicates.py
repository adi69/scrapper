import csv
import sys

with open(sys.argv[1], 'rb') as f:
    x = list(csv.reader(f))

h = {}
flag = True
count = 0

for i in x:
    if i[1] in h:
        print "\n\nFUCK, MAN! ======= DUPLICACY FOUND! ======= ", i[1]
        flag = False
    else:
        h[i[1]] = True

if flag == True: print "\n\n===== YESS! No Duplicates Found!! ====="  
print "Total records = ", len(h)
