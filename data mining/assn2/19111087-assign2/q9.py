

import pandas as pd
from urllib.parse import unquote



def title_parse(title):
    title = unquote(title)
    return title


columns = ['article','category']
df = pd.read_csv('wikispeedia_paths-and-graph/categories.tsv',delimiter='\t',encoding='UTF-8',skiprows=12,header=None,names=columns)
df['article']= df.article.apply(title_parse)


columns = ['category','ID']
df2 = pd.read_csv('category-ids.csv',names=columns)


categories = list((df2['category']))
ID = list((df2['ID']))
cat_ID_dict = dict()
cat_child_dict = dict()

for i in range(len(categories)):
    cat_ID_dict[categories[i]]=ID[i]
    cat_child_dict[ID[i]]=list()
    
for categ in categories:
    
    categ_split = categ.split('.')
    temp = "subject"
    temp_ID = cat_ID_dict[temp]
    
    for i in range(len(categ_split)):
        
        if i!=0:
            temp_next = temp + "." + categ_split[i]
            temp_next_ID = cat_ID_dict[temp_next]
            #print(temp_next,temp_next_ID,temp,temp_ID)
            cat_child_dict[temp_ID].append(temp_next_ID)
            temp = temp_next
            temp_ID = temp_next_ID
            
for i in range(len(ID)):
    cat_child_dict[ID[i]]=set(cat_child_dict[ID[i]])
    

columns =['categories', 'paths','visited','shortest_paths','shortest_visited']
df3 = pd.read_csv('category-paths.csv',names=columns)

categories = list(df3['categories'])
paths = list(df3['paths'])
visited = list(df3['visited'])
shortest_paths = list(df3['shortest_paths'])
shortest_visited = list(df3['shortest_visited'])


l0=[]
l1=[]
l2=[]
l3=[]

categories=list(set(df['category']))

for categ in categories:
    
    categ_split = categ.split('.')
    temp = ""
    for i in range(len(categ_split)):
        temp = temp + "." + categ_split[i]
        temp_s = temp[1:].split('.')
            
        if len(temp_s)==1:
            l0.append(temp[1:])
        elif len(temp_s)==2:
            l1.append(temp[1:])
        elif len(temp_s)==3:
            l2.append(temp[1:])
        elif len(temp_s)==4:
            l3.append(temp[1:])
            
l0 =  list(set(l0))
l2 =  list(set(l2))
l3 =  list(set(l3))
l1 =  list(set(l1))

ll = l2 + l1 + l0



categories = list((df2['ID']))
for parent in ll:
    parent_ID = cat_ID_dict[parent]
    
    for child in cat_child_dict[parent_ID]:
        idx = int(parent_ID[1:])-1
        c_idx = int(child[1:])-1
        paths[idx] += paths[c_idx]
        visited[idx] += visited[c_idx]
        shortest_paths[idx] += shortest_paths[c_idx]
        shortest_visited[idx] += shortest_visited[c_idx]
    

df4 = pd.DataFrame(list(zip(categories,paths,visited,shortest_paths,shortest_visited)), columns =['categories', 'paths','visited','shortest_paths','shortest_visited']) 


df4.to_csv('category-subtree-paths.csv',index=False,header=None)

