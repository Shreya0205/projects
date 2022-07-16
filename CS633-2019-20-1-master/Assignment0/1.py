 
import matplotlib.pyplot as plt
import numpy as np


data=[0.000011,0.000015,0.000078,0.000027,0.000031,0.000053,0.000062,0.000030,0.000030,0.000028]

fig=plt.figure(1, figsize=(7,7))

ax=fig.add_subplot(111)
bp=ax.boxplot(data)

bp = ax.boxplot(data, patch_artist=True)
for box in bp['boxes']:
    box.set( color='#7570b3', linewidth=2)
    box.set( facecolor = '#1b9e77' )
    
for whisker in bp['whiskers']:
    whisker.set(color='#7570b3', linewidth=2)


for cap in bp['caps']:
    cap.set(color='#7570b3', linewidth=2)


for median in bp['medians']:
    median.set(color='#b2df8a', linewidth=2)

plt.ylabel('Time (in sec)')
plt.xlabel('Single Host')
plt.show()
