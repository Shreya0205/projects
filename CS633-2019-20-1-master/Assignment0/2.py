 
import matplotlib.pyplot as plt
import numpy as np


data=[0.000656,0.001183,0.001048,0.002967,0.001598,0.003412,0.004257,0.001134,0.003680,0.001216]

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
plt.xlabel('Two Hosts with 2 process per node')
plt.show()
