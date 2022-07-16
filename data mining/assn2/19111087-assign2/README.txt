# CS685: Data Mining Assignment 2
The assignment makes use of the data available at http://snap.stanford.edu/data/wikispeedia.html. 

***Every Output file must be deleted before executing the code.***

## Dependencies and libraries required for the entire assignment:
- python3
- pandas
- numpy

## Help log
The entire assignment can be executed using assign2.sh file. 
```
usage: bash assign2.sh
```
- To excute individual program, separate shell scripts (.sh file) are also provided.


## question1 
```
usage: bash q1.sh
```
- It augment the names of the articles to have ids from A0001 to A4604.
- It outputs the article-ids.csv.


## question2
```
usage: bash q2.sh
```
- It converts categories of the articles into a hierarchy (Starting from subject), assigning them ids starting from C0001 till the end using breadth-first ordering with the children ordered in alphabetical order
- It outputs category-ids.csv.


## question3
```
usage: bash q3.sh
```
- It Augment the article-ids.csv file to include all the categories the corresponding article is in.
- It outputs article-categories.csv.


## question4
```
usage: bash q4.sh
```
- It output this as edges.csv in an adjacency list format. 
- Assuming graph is directed. Edges are added as it comes. If an edge from a->b is there then b->a is not added into the output unless it is their in shortest path matrix with distance 1.


## question5
```
usage: bash q5.sh
```
- It outputs graph-components.csv containing number of components, number of edges in each component, and their diameter.
- Used strongly connected components algo (Tarjan's algo) assuming the graph as directed graph.
 

*** Paths with length greater than 2 are considered, path with only one article is ignored and all category pairs are considered of source and destination ***

## question6
```
usage: bash q6.sh
```
- It outputs finished-paths-no-back.csv and finished-paths-back.csv
- For each finished path, It calculates length of path traversed by human, length of shortest path, ratio of human path to shortest path.


## question7
```
usage: bash q7.sh
```
- It outputs percentage-paths-no-back.csv and percentage-paths-back.csv.
- It outputs percentage of human paths that have:
1. Exactly the same path length as the shortest path
2. Path length is 1 to 10 more than the shortest path (each separately)
3. Path length is 11 or more than the shortest path


## question8
```
usage: bash q8.sh
```
- It outputs category-paths.csv.
- For each category, it outputs the number of paths that it visited, and number of times it visited.


## question9
```
usage: bash q9.sh
```
- It outputs category-subtree-paths.csv.


## question10
```
usage: bash q10.sh
```
- It outputs category-pairs.csv.
- Some of the articles had wrong spellings and some had no relation to any of the articles so such articles are assigned 'subject' categories.
- Below list had no article, so these are assigned subject category.
l=['Long_peper','Test','Bogota','Adolph_Hitler','English','Kashmir','Podcast','Christmas','Mustard','Sportacus','Charlottes_web','Macedonia','Fats','Usa','_Zebra','Rss','Western_Australia','The_Rock','Georgia','Netbook','Black_ops_2','Great','The','Rat']


## question11
```
usage: bash q11.sh
```
- It outputs category-ratios.csv.

