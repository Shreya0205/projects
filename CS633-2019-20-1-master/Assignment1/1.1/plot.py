import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import statistics


f=np.loadtxt("datafile.txt")


data1=f[1:5]
data2=f[5:10]
data3=f[11:15]
data4=f[16:20]
data5=f[20:25]


data=[data1,data2,data3,data4,data5]

fig=plt.figure(1)
ax=fig.add_subplot(111)
bp=ax.boxplot(data, patch_artist=True,labels=['.000128 MB', '.001024 MB','.065536 MB','1.048576 MB','4.194304 MB'])


for box in bp['boxes']:
    box.set( color='#7570b3', linewidth=2)
    box.set( facecolor = '#1b9e77' )

plt.xlabel('Data in MB')
plt.ylabel('Bandwidth in MBps')

y_number_values=[statistics.median(data1),statistics.median(data2),statistics.median(data3),statistics.median(data4),statistics.median(data5)]
x_number_values=[1,2,3,4,5]
plt.plot(x_number_values, y_number_values, linewidth=1,label='Blocking N=2')


lgd=plt.legend( loc="upper center",bbox_to_anchor=(1.3,0.5), shadow=True, fancybox=True)
plt.savefig("plot.jpg",bbox_extra_artists=(lgd,), bbox_inches='tight')


