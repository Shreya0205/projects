
import pandas as pd
from urllib.parse import unquote


def title_parse(title):
    title = unquote(title)
    return title


columns = ['article','ID']
df = pd.read_csv('article-ids.csv',names=columns)
df['article']= df.article.apply(title_parse)

i=1
from_list=[]
to_list=[]

with open('wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt') as f:
    
    for _ in range(17):
        next(f)
    
    for line in f:
        
        i_=str(i)
        if len(i_) == 1:
            i_ = ("A000"+i_)
        elif len(i_)==2:
            i_ = ("A00"+i_)
        elif len(i_)==3:
            i_ = ("A0"+i_)
        else:
            i_ = ("A"+i_)
                    
        for to_ in range(len(line)-1):
            
            
            if line[to_]==str(1):
                
                #print(line[to_])
                from_list.append(i_)   
                to = str(to_+1)
                if len(to) == 1:
                    to_list.append("A000"+to)
                elif len(to)==2:
                    to_list.append("A00"+to)
                elif len(to)==3:
                    to_list.append("A0"+to)
                else:
                    to_list.append("A"+to)
              
                
        i=i+1




df = pd.DataFrame(list(zip(from_list, to_list)), columns =['From', 'To']) 


df.to_csv('edges.csv',index=False,header=None)

