import json 
import pandas as pd


with open('neighbor-districts-modified.json') as json_data:
    graph = json.load(json_data)


with open('mapping.json') as json_data:
    mapping = json.load(json_data)


## appending idx if two districts are neighbors in neighbor.json file
def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append([mapping[node], mapping[neighbour]])
    return edges

edges = generate_edges(graph)

df = pd.DataFrame(edges)
df.to_csv('edge-graph.csv', index=False, header=False)

print("Edge graph generated")
