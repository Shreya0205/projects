import json
import csv 
import numpy as np

## mapping.json contains mapping of district name to id
with open('mapping.json') as json_data:
    mapping = json.load(json_data)


## common function to find zscore of all other districts in a state depending upon which metric you choose i.e weekly, monthy or overall
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
    
    ## calculating the zscore with the help of above dictionaries neighbor and state wise and writing it into file
    for district in mapping.keys():
        idx = mapping[district]
        for metric_num in metric_list:
            
            dist_case = metric_dict[idx][metric_num]
            neighbor_mean_std = neighbor_metric_dict[idx][metric_num]
            state_mean_std = state_metric_dict[idx][metric_num]
            
            ## if s.d. is zero, then storing nan as zscore value
            if float(neighbor_mean_std[1])==0:
                zscore_neighbor = np.nan
            else:
                zscore_neighbor = round((dist_case - float(neighbor_mean_std[0]))/float(neighbor_mean_std[1]),2)
            
            if float(state_mean_std[1])==0:
                zscore_state = np.nan
            else:
                zscore_state = round((dist_case - float(state_mean_std[0]))/float(state_mean_std[1]),2)

            f.write(str(idx)+","+str(metric_num)+","+str(zscore_neighbor)+","+str(zscore_state)+"\n")

    f.close()
        

neighbors_creation('cases-week.csv','neighbor-week.csv','state-week.csv','zscore-week.csv')
neighbors_creation('cases-month.csv','neighbor-month.csv','state-month.csv','zscore-month.csv')
neighbors_creation('cases-overall.csv','neighbor-overall.csv','state-overall.csv','zscore-overall.csv')


print("Zscore file generated")
