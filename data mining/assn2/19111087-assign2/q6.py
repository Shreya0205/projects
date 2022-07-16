
import pandas as pd
import math
from urllib.parse import unquote
from collections import deque  


def title_parse(title):
    title = unquote(title)
    return title


columns = ['hashedIpAddress','timestamp','durationInSec','path','rating']
df = pd.read_csv('wikispeedia_paths-and-graph/paths_finished.tsv',delimiter='\t',encoding='UTF-8',skiprows=16,header=None,names=columns)
df['path']= df.path.apply(title_parse)


columns = ['article','ID']
df2 = pd.read_csv('article-ids.csv',names=columns)
df2['article']= df2.article.apply(title_parse)


columns = ['article','ID']
df3 = pd.read_csv('article-ids.csv',names=columns)
df3['article'] = df3.article.apply(title_parse)

art_ID = dict()

data = df3['article']
data_ID = df3['ID']

for i in range(len(data)):
    art_ID[data[i]]=data_ID[i]
       


f = open('wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt')
lines = f.readlines()



human_path = []
shortest_path = []
ratio = []

for index, row in df.iterrows():
    
    path_ = row['path']
    path_ = path_.split(';')
    
    #path_ = [i for i in path_ if i != "<"] 
    
    s = path_[0]
    d = path_[-1]
    
    if len(path_)>=2:
        
        s1 = int(art_ID[s][1:])
        d1 = int(art_ID[d][1:])
        
        if lines[s1+16][d1-1]!='_':
            shortest_path.append(int(lines[s1+16][d1-1]))
            human_path.append(len(path_)-1)
            ratio.append(human_path[-1]/shortest_path[-1])
    


human_path2 = []
shortest_path2 = []
ratio2 = []

for index, row in df.iterrows():
    
    path_ = row['path']
    path_ = path_.split(';')
    
    queue = deque()
    
    for i in path_:
        if i!='<':
            queue.append(i)
        else:
            queue.pop()
    
    path_ = list(queue)
        
    s = path_[0]
    d = path_[-1]
    
    if len(path_)>=2:

        s1 = int(art_ID[s][1:])
        d1 = int(art_ID[d][1:])
        
        if lines[s1+16][d1-1]!='_':
            shortest_path2.append(int(lines[s1+16][d1-1]))
            human_path2.append(len(path_)-1)
            ratio2.append(human_path2[-1]/shortest_path2[-1])
    

df3 = pd.DataFrame(list(zip(human_path, shortest_path, ratio)), columns =['human_path', 'shortest_path', 'ratio']) 
df3.to_csv('finished-paths-back.csv',index=False,header=None)



df4 = pd.DataFrame(list(zip(human_path2, shortest_path2, ratio2)), columns =['human_path', 'shortest_path', 'ratio']) 
df4.to_csv('finished-paths-no-back.csv',index=False,header=None)

