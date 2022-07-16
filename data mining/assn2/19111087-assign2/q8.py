
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
df=df.drop([2395])

columns = ['category','ID']
df2 = pd.read_csv('category-ids.csv',names=columns)

categories = list(df2['ID'])
paths = [0]*len(categories)
visited = [0]*len(categories)
shortest_paths = [0]*len(categories)
shortest_visited = [0]*len(categories)


columns = ['article','ID']
df3 = pd.read_csv('article-ids.csv',names=columns)
df3['article'] = df3.article.apply(title_parse)

art_ID = dict()

data = df3['article']
data_ID = df3['ID']

for i in range(len(data)):
    art_ID[data[i]]=data_ID[i]
       



art_category = dict()

data = open('article-categories2.csv', 'r') 
for line in data:
    line = line.split(',')
    
    for i in range(len(line)):
        if i==0:
            if line[i] not in art_category.keys():
                art_category[line[i]]=list()
        else:
            art_category[line[0]].append(line[i].strip())

data.close()



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
        
    
    
    if len(path_)>=2:
        temp = {}
        for art in path_:

            art_id = art_ID[str(art)]

            for cat in art_category[art_id]:

                cat_i=int(cat[1:])-1
                if cat not in temp.keys():
                    temp[cat]=0
                    paths[cat_i]=paths[cat_i]+1
                    temp[cat]=1

                visited[cat_i]=visited[cat_i]+1
        
        
        s=path_[0]
        d=path_[-1]
        temp = {}
    
    
        art_id_s = art_ID[str(s)]
        art_id_d = art_ID[str(d)]
        
        for cat in art_category[art_id_s]:
            cat_i=int(cat[1:])-1
            if cat not in temp.keys():
                temp[cat]=0
                shortest_paths[cat_i]=shortest_paths[cat_i]+1
                temp[cat]=1
                
            shortest_visited[cat_i]=shortest_visited[cat_i]+1
        
        for cat in art_category[art_id_d]:
            cat_i=int(cat[1:])-1
            if cat not in temp.keys():
                temp[cat]=0
                shortest_paths[cat_i]=shortest_paths[cat_i]+1
                temp[cat]=1
                
            shortest_visited[cat_i]=shortest_visited[cat_i]+1


df2 = pd.DataFrame(list(zip(categories,paths,visited,shortest_paths,shortest_visited)), columns =['categories', 'paths','visited','shortest_paths','shortest_visited']) 

df2.to_csv('category-paths.csv',index=False,header=None)

