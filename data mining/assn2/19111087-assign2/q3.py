

import pandas as pd
from urllib.parse import unquote
import pickle



def title_parse(title):
    title = unquote(title)
    return title


columns = ['article','ID']
df = pd.read_csv('article-ids.csv',names=columns)
df['article']= df.article.apply(title_parse)


columns = ['article','category']
df2 = pd.read_csv('wikispeedia_paths-and-graph/categories.tsv',delimiter='\t',encoding='UTF-8',skiprows=12,header=None,names=columns)
df2['article']= df2.article.apply(title_parse)


columns = ['category','ID']
df3 = pd.read_csv('category-ids.csv',names=columns)


art_category = dict()

for index, row in df.iterrows():
    art_ID = row['ID']
    art_category[art_ID]=list()
    
for index, row in df2.iterrows():

    art = row['article']
    cat = row['category']
    
    art_ID = list(df.loc[df['article'] == art]['ID'])
    cat_ID = list(df3.loc[df3['category'] == cat]['ID'])
    
    art_category[art_ID[0]].append(cat_ID[0])
    
for item in art_category.keys():
    
    if len(art_category[item])==0:
        art_category[item].append('C0001')
        


f = open('article-categories.csv', 'a')
f.write('Article_ID,category_ID\n')

for item in art_category.keys():
    
    cat="'"
    
    for i in art_category[item]:
        if len(cat)==1:
            cat = cat + str(i)
        else:
            cat = cat +"," + str(i)
            
    cat = cat + "'"
        
    f.write(item +','+ cat + '\n')
    
f.close()


f = open('article-categories2.csv', 'a')

for item in art_category.keys():
    f.write(item +','+ ','.join(art_category[item])+'\n')
    
f.close()

