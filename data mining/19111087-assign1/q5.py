import json
import csv 
import numpy as np

## mapping.json contains mapping of district name to id
with open('mapping.json') as json_data:
    mapping = json.load(json_data)
    
with open('neighbor-districts-modified.json') as json_data:
    neighbors = json.load(json_data)
    

## common function to find mean and s.d. of all other districts in a state depending upon which metric you choose i.e weekly, monthy or overall
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
    
    f=open(outfile_name,'a')

    ## for a district, every other district is checked if it is in the same state, and their mean and s.d is calculated
    for district in mapping.keys():
        
        state = district.split("_")[1]
        idx = mapping[district]
        
        for metric_num in metric_list:
            
            count=[]

            for state_dist in mapping.keys():
                
                other_dist_state = state_dist.split("_")[1]
                other_dist_idx = mapping[state_dist]
                
                if state==other_dist_state and other_dist_idx!=idx:
                    count.append(metric_dict[other_dist_idx][metric_num])
            
            
            if len(count)==0 :
                std=0
                mean=0
            else:
                std = round(np.std(count),2)
                mean = round(np.mean(count),2)

            f.write(str(idx)+","+str(metric_num)+","+str(mean)+","+str(std)+"\n")

    f.close()
    

neighbors_creation('cases-week.csv','state-week.csv')
neighbors_creation('cases-month.csv','state-month.csv')
neighbors_creation('cases-overall.csv','state-overall.csv')

print("Mean and s.d. of neighbors in the same state file generated")
