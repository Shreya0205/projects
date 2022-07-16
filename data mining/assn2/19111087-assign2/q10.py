
import pandas as pd
import math
from urllib.parse import unquote
from collections import deque  


def title_parse(title):
    title = unquote(title)
    return title



columns = ['hashedIpAddress','timestamp','durationInSec','path','target','type']
df = pd.read_csv('wikispeedia_paths-and-graph/paths_unfinished.tsv',delimiter='\t',encoding='UTF-8',skiprows=16,header=None,names=columns)
df['path']= df.path.apply(title_parse)
df['target']= df.target.apply(title_parse)

columns = ['hashedIpAddress','timestamp','durationInSec','path','rating']
df_f = pd.read_csv('wikispeedia_paths-and-graph/paths_finished.tsv',delimiter='\t',encoding='UTF-8',skiprows=16,header=None,names=columns)
df_f['path']= df_f.path.apply(title_parse)


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


columns = ['article','ID']
df3 = pd.read_csv('article-ids.csv',names=columns)
df3['article'] = df3.article.apply(title_parse)

art_ID = dict()

data = df3['article']
data_ID = df3['ID']

for i in range(len(data)):
    art_ID[data[i]]=data_ID[i]


columns = ['category','ID']
df2 = pd.read_csv('category-ids.csv',names=columns)
cat_ID = dict()

data = df2['category']
data_ID = df2['ID']

for i in range(len(data)):
    cat_ID[data[i]]=data_ID[i]
    
ID_cat = dict()

for i in range(len(data)):
    cat_ID[data_ID[i]]=data[i]



category_pair = {}
ID = list((df2['ID']))

for i in ID:
    category_pair[i]={}
    for j in ID:
        category_pair[i][j]=[0,0]



l=['Long_peper','Test','Bogota','Adolph_Hitler','English','Kashmir','Podcast','Christmas','Mustard','Sportacus','Charlottes_web','Macedonia','Fats','Usa','_Zebra','Rss','Western_Australia','The_Rock','Georgia','Netbook','Black_ops_2','Great','The','Rat']




for index, row in df.iterrows():
    
    path_ = row['path']
    s = path_.split(';')[0]
    d = row['target']
    
    if s in l:
        s_cat = ['C0001']
    else:
        s_idx = art_ID[s]
        s_cat = art_category[s_idx]
    
    if d in l:
        d_cat = ['C0001']
    else:
        d_idx = art_ID[d]
        d_cat = art_category[d_idx]
    
    scat = [cat_ID[idx] for idx in s_cat]
    dcat = [cat_ID[idx] for idx in d_cat]
    
    s=[]
    d=[]
    
    for sf in scat:
        sf = sf.split('.')
        temp=""
        
        for i in range(len(sf)):
            
            if i==0:
                s.append('C0001')
                temp="subject"
            else:
                temp=temp+"."+sf[i]
                s.append(cat_ID[temp])
                
    
    for sf in dcat:
        sf = sf.split('.')
        temp=""
        for i in range(len(sf)):
            if i==0:
                d.append('C0001')
                temp="subject"
            else:
                temp=temp+"."+sf[i]
                d.append(cat_ID[temp])
            
    for cat_id in s:
        for d_cat_id in d:
            category_pair[cat_id][d_cat_id][0]=category_pair[cat_id][d_cat_id][0]+1
            
            


for index, row in df_f.iterrows():
    
    path_ = row['path']
    s = path_.split(';')[0]
    d = path_.split(';')[-1]
    
    s_idx = art_ID[s]
    s_cat = art_category[s_idx]
    
    d_idx = art_ID[d]
    d_cat = art_category[d_idx]
    
    scat = [cat_ID[idx] for idx in s_cat]
    dcat = [cat_ID[idx] for idx in d_cat]
    
    s=[]
    d=[]
    
    for sf in scat:
        sf = sf.split('.')
        temp=""
        
        for i in range(len(sf)):
            
            if i==0:
                s.append('C0001')
                temp="subject"
            else:
                temp=temp+"."+sf[i]
                s.append(cat_ID[temp])
                
    
    for sf in dcat:
        sf = sf.split('.')
        temp=""
        for i in range(len(sf)):
            if i==0:
                d.append('C0001')
                temp="subject"
            else:
                temp=temp+"."+sf[i]
                d.append(cat_ID[temp])
                
    for cat_id in s:
        for d_cat_id in d:
            category_pair[cat_id][d_cat_id][1]=category_pair[cat_id][d_cat_id][1]+1
            
            


f=open('category-pairs.csv','a')

for s in category_pair.keys():
    for d in category_pair[s].keys():
        
        unfi=category_pair[s][d][0]
        fi=category_pair[s][d][1]
        
        if unfi+fi!=0:
            f.write(str(s)+","+str(d)+","+str((unfi*100)/(unfi+fi))+","+str((fi*100)/(unfi+fi))+"\n")

f.close()

