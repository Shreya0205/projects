import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics 

labels = ['.001024 MB','.065536 MB', '.262144 MB', '1.048576 MB']


i=0
while(i<6):

   
    data=[]
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    
    filename= "datafile"
    filename=filename +str(i+1)
    filename=filename +".txt"
    
    f=np.loadtxt(filename)
    
    data1=f[1:5]
    data2=f[5:10]
    data3=f[11:15]
    data4=f[16:20]

    data=[data1,data2,data3,data4]
    ##plt.boxplot(data, showmeans=True, patch_artist=True, labels=labels)

    fig=plt.figure(1)
    ax=fig.add_subplot(111)
    bp=ax.boxplot(data, patch_artist=True,labels=labels)


    for box in bp['boxes']:
        box.set( color='#7570b3', linewidth=2)
        box.set( facecolor = '#1b9e77' )

    y_number_values=[statistics.median(data1),statistics.median(data2),statistics.median(data3),statistics.median(data4)]
    x_number_values=[1,2,3,4]
    
    if(i==0):
      plt.plot(x_number_values, y_number_values, 'r-', linewidth=1,label='Blocking N=8')
    elif(i==1):
      plt.plot(x_number_values, y_number_values, 'b-', linewidth=1,label='Non-Blocking N=8')
    elif(i==2):
      plt.plot(x_number_values, y_number_values, 'g-', linewidth=1,label='Blocking N=16')
    elif(i==3):
      plt.plot(x_number_values, y_number_values,'y-', linewidth=1,label='Non-Blocking N=16')
    elif(i==4):
      plt.plot(x_number_values, y_number_values, 'o-',linewidth=1,label='Blocking N=32')
    elif(i==5):
      plt.plot(x_number_values, y_number_values, 'p-', linewidth=1,label='Non-Blocking N=32')

    i=i+1

plt.xlabel('Data (MBs)')
lgd=plt.legend( loc="upper center",bbox_to_anchor=(1.3,0.5), shadow=True, fancybox=True)
plt.savefig("plot.jpg",bbox_extra_artists=(lgd,), bbox_inches='tight')

