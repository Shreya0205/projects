import json
import csv 
import numpy as np

## mapping.json contains mapping of district name to id
with open('mapping.json') as json_data:
    mapping = json.load(json_data)


## common function to find the hotspot and coldspot districts with metric value as week, month, or overall 
def neighbors_creation(file_name, file_name1, file_name2, outfile_name):
    

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
    

    ## neighbor_metric_dict contains mean and s.d for the neighbor districts for the metric you provided
    ## metric is week, month or overall
    neighbor_metric_dict = dict()
    for dist in mapping.values():
        neighbor_metric_dict[dist]=dict()     
    data = open(file_name1, 'r') 
    neighbor_metric_list = set()
    for line in data:
        line = line.split(',')
        neighbor_metric_list.add(int(line[1]))
        ## for metric num(week number or month number or overall num)
        neighbor_metric_dict[int(line[0])][int(line[1])] = list()
        ## storing mean
        neighbor_metric_dict[int(line[0])][int(line[1])].append((line[2]))
        ## storing s.d.
        neighbor_metric_dict[int(line[0])][int(line[1])].append((line[3]))
    data.close()
    neighbor_metric_list=list(neighbor_metric_list)
    neighbor_metric_list.sort()
    

    ## state_metric_dict contains mean and s.d for the districts for all the other sitricts in the state for the metric you provided
    ## metric is week, month or overall
    state_metric_dict = dict()
    for dist in mapping.values():
        state_metric_dict[dist]=dict()
    data = open(file_name2, 'r') 
    state_metric_list = set()
    for line in data:
        line = line.split(',')
        state_metric_list.add(int(line[1]))
        ## for metric num(week number or month number or overall num)
        state_metric_dict[int(line[0])][int(line[1])] = list()
        ## storing mean
        state_metric_dict[int(line[0])][int(line[1])].append((line[2]))
        ## storing s.d.
        state_metric_dict[int(line[0])][int(line[1])].append((line[3]))
    data.close()
    state_metric_list=list(state_metric_list)
    state_metric_list.sort()
    
    
    f=open(outfile_name,'a')  
    
    ## for every district and for the corresponding metric number for neighbors(week no, month no, or overall), upper value(mean+sd) and lower value(mean-sd) is calculated
    for district in mapping.keys():
        idx = mapping[district]
        
        for metric_num in metric_list:
            
            dist_case = metric_dict[idx][metric_num]
            neighbor_mean_std = neighbor_metric_dict[idx][metric_num]
            
            upper_value = float(neighbor_mean_std[0]) + float(neighbor_mean_std[1])
            lower_value = float(neighbor_mean_std[0]) - float(neighbor_mean_std[1])
            
            ## checking the district is hotspot or coldspot among its neighbors
            if dist_case > upper_value:
                f.write(str(metric_num)+",neighborhood,hot,"+str(idx)+"\n")
            elif dist_case < lower_value:
                f.write(str(metric_num)+",neighborhood,cold,"+str(idx)+"\n")
       

    ## for every district and for the corresponding metric number for districts in states(week no, month no, or overall), upper value(mean+sd) and lower value(mean-sd) is calculated
    for district in mapping.keys():
        idx = mapping[district]
        
        for metric_num in metric_list:
            
            dist_case = metric_dict[idx][metric_num]
            state_mean_std = state_metric_dict[idx][metric_num]
            
            upper_value = float(state_mean_std[0]) + float(state_mean_std[1])
            lower_value = float(state_mean_std[0]) - float(state_mean_std[1])

            ## checking the district is hotspot or coldspot among its neighbors
            if dist_case > upper_value:
                f.write(str(metric_num)+",state,hot,"+str(idx)+"\n")
            elif dist_case < lower_value:
                f.write(str(metric_num)+",state,cold,"+str(idx)+"\n")
                
               
    f.close()
        

neighbors_creation('cases-week.csv','neighbor-week.csv','state-week.csv','method-spot-week.csv')
neighbors_creation('cases-month.csv','neighbor-month.csv','state-month.csv','method-spot-month.csv')
neighbors_creation('cases-overall.csv','neighbor-overall.csv','state-overall.csv','method-spot-overall.csv')

print("District is hotspot/coldspot file generated")
