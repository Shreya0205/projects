
import pandas as pd
import numpy as np 
from scipy.sparse import csr_matrix 


columns = ['From','To']
df = pd.read_csv('edges.csv',names=columns)
ids = list(df['From'])

edge_dict = csr_matrix((4605, 4605),dtype = np.int8).toarray() 

for index, row in df.iterrows():
    s = row['From']
    d = row['To']
    s=int(s[1:])
    d=int(d[1:])
    edge_dict[s][d]=1

V = 4605
adj = [[] for i in range(V)]


def DFSUtil(v, visited):
 
    visited[v] = True
 
    for i in adj[v]:
        if visited[i] == False:
            DFSUtil(i, visited)
        
 
    
def addEdge(v, w):
    #print(int(w[1:]))
    adj[int(v[1:])].append(int(w[1:]))
    #adj[int(w[1:])].append(int(v[1:]))

def connectedComponents():
    visited = []
    cc = []
    temp = 0
    for i in range(V):
        visited.append(False)
    for v in range(V):
        if v==0:
            continue
        if visited[v] == False:
            (DFSUtil(v, visited))
            temp=temp+1
    return temp
        


import sys 
  

sys.setrecursionlimit(10**6) 
from_list = list(df['From'])
to_list = list(df['To'])

for i in range(len(from_list)):
    addEdge(from_list[i],to_list[i])



components=[]
from collections import defaultdict 

temp = 0

class Graph: 
   
    def __init__(self,vertices): 
        self.V= vertices  
        self.graph = defaultdict(list)  
        self.Time = 0
   
    def addEdge(self,u,v): 
        self.graph[int(u[1:])].append(int(v[1:])) 
          
    def SCCUtil(self,u, low, disc, stackMember, st): 
        disc[u] = self.Time 
        low[u] = self.Time 
        self.Time += 1
        stackMember[u] = True
        st.append(u) 
  
        
        for v in self.graph[u]: 
            if disc[v] == -1 : 
                self.SCCUtil(v, low, disc, stackMember, st) 
                low[u] = min(low[u], low[v])           
            elif stackMember[v] == True:
                low[u] = min(low[u], disc[v]) 
  
        w = -1 
        nodes=[]
        global temp
        if low[u] == disc[u]: 
            temp=temp+1
            while w != u: 
                w = st.pop() 
                nodes.append(w)
                
                stackMember[w] = False
                  
            components.append(nodes) 
              
    def SCC(self): 
        disc = [-1] * (self.V) 
        low = [-1] * (self.V) 
        stackMember = [False] * (self.V) 
        st =[] 
          
        for i in range(self.V): 
            if i==0:
                continue
            if disc[i] == -1: 
                self.SCCUtil(i, low, disc, stackMember, st) 
  
  
   
   



import sys 
  

sys.setrecursionlimit(10**6) 
from_list = list(df['From'])
to_list = list(df['To'])

g1 = Graph(4605) 

for i in range(len(from_list)):
    g1.addEdge(from_list[i],to_list[i])

g1.SCC() 

    




f = open('wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt')
lines = f.readlines()




nodes = []
edges = []
diameter = []

for ll in range(len(components)):
    
    temp = list(set(components[ll]))
    ln = len(temp)
    nodes.append(ln)
    index = dict()
    
    if ln==1:
        edges.append(0)
        diameter.append(0)
        
    else:
        
        edge = []
        ed_l = 0
        
        mat = np.full((ln, ln), np.inf)
        
        for s in temp:
            for d in temp:
                if s!=d:
                    if edge_dict[s][d]==1:
                        ed_l = ed_l+1
           
        edges.append(ed_l)
        dia=0
        
        for k in temp:
            for i in temp:
                
                if lines[k+16][i-1]!='_':
                    if int(lines[k+16][i-1])>dia:
                        dia=int(lines[k+16][i-1])
                       
                           
        diameter.append(dia)
        
        
        


df3 = pd.DataFrame(list(zip(nodes,edges,diameter)), columns =['nodes','edges','diameter']) 
df3.to_csv('graph-components.csv',index=False,header=None)

