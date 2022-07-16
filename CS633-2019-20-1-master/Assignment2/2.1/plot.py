# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 20:48:21 2019

@author: Sanket
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import sys

filename= "datafile" + str(sys.argv[1]) + ".txt"
f=open(filename)
f1=open('datafile.txt','w')
lines=f.readlines()

for x in range(4,8999,10):
    f1.write(lines[x])

f.close()
f1.close()

matplotlib.rc('figure', figsize=(13, 7))


file = open('datafile.txt', 'r')

X, Y, Z = [], [], [];

for l in file:
    row = l.split()
    X.append(float(row[0].lstrip().rstrip()))
    Y.append(float(row[1].lstrip().rstrip()))
    Z.append(float(row[2].lstrip().rstrip()))

file.close();


data = pd.DataFrame({'X': X, 'Y': Y, 'Z': Z})
data_pivoted = data.pivot("Y", "X", "Z")
ax = sns.heatmap(data_pivoted)

imgname = "plot-" + str(sys.argv[1]) + ".jpg"
plt.savefig(imgname)
plt.show()

