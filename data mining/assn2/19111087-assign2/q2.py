
import pandas as pd
from urllib.parse import unquote


def title_parse(title):
    title = unquote(title)
    return title


columns = ['article','category']
df = pd.read_csv('wikispeedia_paths-and-graph/categories.tsv',delimiter='\t',encoding='UTF-8',skiprows=12,header=None,names=columns)
df['article']= df.article.apply(title_parse)


categories=list(set(df['category']))



l0=[]
l1=[]
l2=[]
l3=[]

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


l1.sort()
l2.sort()
l3.sort()
lls = l0 + l1 + l2 + l3



idx=[]
for i in range(1,len(lls)+1):
    i=str(i)
    if len(i) == 1:
        idx.append("C000"+i)
    elif len(i)==2:
        idx.append("C00"+i)
    elif len(i)==3:
        idx.append("C0"+i)
    else:
        idx.append("C"+i)


f=open('category-ids.csv','w')
for i,j in zip(lls,idx):
    f.write(str(i)+","+str(j)+"\n")
f.close()

