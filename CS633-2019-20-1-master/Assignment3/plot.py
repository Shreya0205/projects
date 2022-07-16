import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics 
import sys

labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

k = sys.argv[1]

i=1

while(i<4):
    
   
    data=[]
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    data5=[]
    data6=[]
    data7=[]
    data8=[]
    data9=[]
    data10=[]
    data11=[]
    data12=[]
    data13=[]
    data14=[]
    data15=[]

    
    if(int(sys.argv[1])):
        filename= "data1/datafile"
    else:
        filename= "data2/datafile"
    
    filename=filename +str(i)
    filename=filename +".txt"
    
    f=np.loadtxt(filename)
    
    data1=f[1:5]
    data2=f[5:10]
    data3=f[11:15]
    data4=f[16:20]
    data5=f[20:25]
    data6=f[25:30]
    data7=f[30:35]
    data8=f[35:40]
    data9=f[40:45]
    data10=f[45:50]
    data11=f[50:55]
    data12=f[55:60]
    data13=f[60:65]
    data14=f[65:70]
    data15=f[70:75]



    data=[data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15]
    ##plt.boxplot(data, showmeans=True, patch_artist=True, labels=labels)

    fig=plt.figure(1)
    ax=fig.add_subplot(111)
    bp=ax.boxplot(data, patch_artist=True,labels=labels)


    for box in bp['boxes']:
        box.set( color='#7570b3', linewidth=2)
        box.set( facecolor = '#1b9e77' )

    y_number_values=[statistics.median(data1),statistics.median(data2),statistics.median(data3),statistics.median(data4),statistics.median(data5),statistics.median(data6),statistics.median(data7),statistics.median(data8),statistics.median(data9),statistics.median(data10),statistics.median(data11),statistics.median(data12),statistics.median(data13),statistics.median(data14),statistics.median(data15)]
    x_number_values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    
    if(i==1):
      plt.plot(x_number_values, y_number_values, 'r-', linewidth=1,label='Pre-Processing Time')
    elif(i==2):
      plt.plot(x_number_values, y_number_values, 'b-', linewidth=1,label='Processing Time')
    elif(i==3):
      plt.plot(x_number_values, y_number_values, 'g-', linewidth=1,label='Total Time')

    i=i+1

plt.xlabel('Number of Processes')
lgd=plt.legend( loc="upper center",bbox_to_anchor=(1.3,0.5), shadow=True, fancybox=True)


if(int(sys.argv[1])):
    plt.savefig("cse/data1/plot.jpg",bbox_extra_artists=(lgd,), bbox_inches='tight')
else:
    plt.savefig("cse/data2/plot.jpg",bbox_extra_artists=(lgd,), bbox_inches='tight')

