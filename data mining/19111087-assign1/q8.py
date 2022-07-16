import json
import csv 
import numpy as np


## mapping.json contains mapping of district name to id
with open('mapping.json') as json_data:
    mapping = json.load(json_data)


## common function to find top 5 hotspot/coldspot depending upon which metric you choose i.e weekly, monthy or overall and for the method state/neighbor
def neighbors_creation(file_name, outfile_name):
    

    ## metric_dict contains zscore for the districts for the metric you provided
    ## metric is week, month or overall number
    metric_dict = dict()
    for dist in mapping.values():
        metric_dict[dist]=dict()     
    data = open(file_name, 'r') 
    metric_list = set()
    for line in data:
        line = line.split(',')
        metric_list.add(int(line[1]))
        ## for metric num(week number or month number or overall num)
        metric_dict[int(line[0])][int(line[1])] = list()
        ## storing mean
        metric_dict[int(line[0])][int(line[1])].append((line[2]))
        ## storing s.d.
        metric_dict[int(line[0])][int(line[1])].append((line[3]))
    data.close()
    metric_list=list(metric_list)
    metric_list.sort()
      
        
    
    f=open(outfile_name,'a')  
    
    ## for a metric number(week number or month number or overall) and for neighbors
    for metric_num in metric_list:
        
        zscore_neighbor_list=list()
        idx_list1=list()
        
        ## for all districts
        for idx in mapping.values(): 
            zscore = metric_dict[idx][metric_num]
            
            ## getting the zscore values if it is not nan and appending it to zscore_neighbor_list
            if zscore[0]!='nan':
                zscore_neighbor_list.append(float(zscore[0]))
                ## idx_list1 contains the district ids for the appended zscore value
                idx_list1.append(idx)
                
        zscore_neighbor_list = np.array(zscore_neighbor_list) 
        
        ## sorting the neighbor zscore values and getting the top and lowest 5 values
        neighbor_ind_hot = np.array(np.argpartition(zscore_neighbor_list,-5)[-5:])
        neighbor_ind_cold = np.array(np.argpartition(zscore_neighbor_list,5)[:5])
       
        ## getting the district ids of the top and lowest 5 zscore values
        neighbor_ind_hot = neighbor_ind_hot[np.argsort(zscore_neighbor_list[neighbor_ind_hot])]
        neighbor_ind_cold = neighbor_ind_cold[np.argsort(zscore_neighbor_list[neighbor_ind_cold])]
       
        idx_list1 = np.array(idx_list1)
        
        f.write(str(metric_num)+",neighborhood,hot,"+str(idx_list1[neighbor_ind_hot][4])+","+str(idx_list1[neighbor_ind_hot][3])+","+str(idx_list1[neighbor_ind_hot][2])+","+str(idx_list1[neighbor_ind_hot][1])+","+str(idx_list1[neighbor_ind_hot][0])+"\n")       
        f.write(str(metric_num)+",neighborhood,cold,"+str(idx_list1[neighbor_ind_cold][4])+","+str(idx_list1[neighbor_ind_cold][3])+","+str(idx_list1[neighbor_ind_cold][2])+","+str(idx_list1[neighbor_ind_cold][1])+","+str(idx_list1[neighbor_ind_cold][0])+"\n")       
      
    
    ## for a metric number(week number or month number or overall) and state wise
    for metric_num in metric_list:
        
        zscore_state_list=list()
        idx_list2=list()

        ## for all districts
        for idx in mapping.values(): 
            zscore = metric_dict[idx][metric_num]
            
            ## getting the zscore values if it is not nan and appending it to zscore_state_list
            if zscore[1]!='nan':
                zscore_state_list.append(float(zscore[1]))
                ## idx_list2 contains the district ids for the appended zscore value
                idx_list2.append(idx)
                
        zscore_state_list = np.array(zscore_state_list) 

        ## sorting the state zscore values and getting the top and lowest 5 values
        state_ind_hot = np.array(np.argpartition(zscore_state_list,-5)[-5:])
        state_ind_cold = np.array(np.argpartition(zscore_state_list,5)[:5])

        ## getting the district ids of the top and lowest 5 zscore values
        state_ind_hot = state_ind_hot[np.argsort(zscore_state_list[state_ind_hot])]
        state_ind_cold = state_ind_cold[np.argsort(zscore_state_list[state_ind_cold])]
       
        idx_list2 = np.array(idx_list2)
              
        f.write(str(metric_num)+",state,hot,"+str(idx_list2[state_ind_hot][4])+","+str(idx_list2[state_ind_hot][3])+","+str(idx_list2[state_ind_hot][2])+","+str(idx_list2[state_ind_hot][1])+","+str(idx_list2[state_ind_hot][0])+"\n")       
        f.write(str(metric_num)+",state,cold,"+str(idx_list2[state_ind_cold][4])+","+str(idx_list2[state_ind_cold][3])+","+str(idx_list2[state_ind_cold][2])+","+str(idx_list2[state_ind_cold][1])+","+str(idx_list2[state_ind_cold][0])+"\n")       
      
    f.close()
        
neighbors_creation('zscore-week.csv','top-week.csv')
neighbors_creation('zscore-month.csv','top-month.csv')
neighbors_creation('zscore-overall.csv','top-overall.csv')

print("Top 5 hot/cold spot file generated")
