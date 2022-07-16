import json
import csv 
import numpy as np

## mapping.json contains mapping of district name to id
with open('mapping.json') as json_data:
    mapping = json.load(json_data)
    
with open('neighbor-districts-modified.json') as json_data:
    neighbors = json.load(json_data)
    


## neighbors_num_dict contains neighbor file replaced with their ids
neighbors_num_dict = dict()

for i in neighbors:
    
    idx = mapping[i]
    neighbors_num_dict[idx] = list()
    
    for j in neighbors[i]:
        
        neigh_idx = mapping[j]
        neighbors_num_dict[idx].append(neigh_idx)
        

## common function to find mean and s.d. of neighbors of a district depending upon which metric you choose i.e weekly, monthy or overall
def neighbors_creation(file_name,outfile_name):
    

    ## metric_dict contains cases for the districts for the metric you provided
    ## metric is week, month or overall
    metric_dict = dict()

    for dist in mapping.values():
        metric_dict[dist]=dict()
        
    data = open(file_name, 'r') 
    metric_list = set()
    for line in data:
        line = line.split(',')
        metric_list.add(int(line[1]))
        metric_dict[int(line[0])][int(line[1])] = int(line[2])

    data.close()

    metric_list=list(metric_list)
    metric_list.sort()
    
    ## n_list lists all districts name  
    n_list = list(neighbors.keys())
    neigh_list = []
    
    for i in n_list:
        idx = mapping[i]
        neigh_list.append(idx)

    ## neigh_list lists sorted district ids
    neigh_list.sort()
    
    f=open(outfile_name,'a')
    
    ## finding the mean and s.d. of neighbors of a district 
    for idx in neigh_list:

        for metric_num in metric_list:
            count=[]

            for neigh_idx in neighbors_num_dict[idx]:
                if idx!=neigh_idx:
                    count.append(metric_dict[neigh_idx][metric_num])

            mean = round(np.mean(count),2)
            std = round(np.std(count),2)

            f.write(str(idx)+","+str(metric_num)+","+str(mean)+","+str(std)+"\n")

    f.close()
        

neighbors_creation('cases-week.csv','neighbor-week.csv')
neighbors_creation('cases-month.csv','neighbor-month.csv')
neighbors_creation('cases-overall.csv','neighbor-overall.csv')

print("Neighbors mean and s.d. file generated")
