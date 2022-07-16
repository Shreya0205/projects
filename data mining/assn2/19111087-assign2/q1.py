

import pandas as pd
from urllib.parse import unquote


def title_parse(title):
    title = unquote(title)
    return title

columns = ['articles']
df = pd.read_csv('wikispeedia_paths-and-graph/articles.tsv',delimiter='\t',encoding='UTF-8',skiprows=11,header=None,names=columns)
df['articles']= df.articles.apply(title_parse)
lst=list(df['articles'])


idx=[]
for i in range(1,4605):
    i=str(i)
    if len(i) == 1:
        idx.append("A000"+i)
    elif len(i)==2:
        idx.append("A00"+i)
    elif len(i)==3:
        idx.append("A0"+i)
    else:
        idx.append("A"+i)


df = pd.DataFrame(list(zip(lst, idx)), columns =['Art','ID']) 
df.to_csv('article-ids.csv',index=False,header=None)




