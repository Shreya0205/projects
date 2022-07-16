
import pandas as pd
import math



def percent_cal(filename, outfilename):
    
    columns =['human_path', 'shortest_path', 'ratio']
    df = pd.read_csv(filename,names=columns)
    
    path=[0,0,0,0,0,0,0,0,0,0,0,0]

    for index, row in df.iterrows():

        path_human = row['human_path']
        path_shortest = row['shortest_path']

        if path_shortest==math.inf or int(path_human)-int(path_shortest)>10:
            path[11]=path[11]+1
        else:
            path[int(path_human)-int(path_shortest)]=path[int(path_human)-int(path_shortest)]+1
    
    newPath = [(i/len(df))*100 for i in path]
    
    newPath = [str(i) for i in newPath]
    
    with open(outfilename, 'w') as outfile:
        outfile.write(','.join(newPath) + '\n')
    

percent_cal('finished-paths-back.csv','percentage-paths-back.csv')
percent_cal('finished-paths-no-back.csv','percentage-paths-no-back.csv')

