 
import matplotlib.pyplot as plt
import numpy as np

data=[0.001792,0.004608,0.001773,0.001616,0.004711,0.001783,0.001898,0.003227,0.001997,0.002480]

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
plt.xlabel('Three hosts with 2 processes per node')
plt.show()
