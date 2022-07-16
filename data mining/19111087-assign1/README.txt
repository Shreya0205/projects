# CS685: Data Mining Assignment 1
The assignment makes use of the data available at https://api.covid19india.org/. The entire data is extracted from https://api.covid19india.org/v4/data-all.json.
The APIs needed to access the data are available at https://api.covid19india.org/.
This assignment outputs the number of confirmed positive covid cases found in a district in a week, month and for the entire duration from 15th april 2020 to 5th sept 2020.
It also calculates the average and standard deviation of cases found in the neighboring/state cities of a district and also outputs the hotspot/coldspot considering neighboring cities or entire states in a week/month/entire duration.
Comments are provided in every python file for the better understanding of the code.


## Dependencies and libraries required for the entire assignment:
- python3
- pandas
- numpy

"""BEFORE EXECUTING THE ASSIGNMENT, ALL OUTPUT FILES MUST BE DELETED(ques2 to ques8 output files, and mapping.json) EXCEPT data-all.json, modified-neighbor.json, all python files and shell files """


## Help log
The entire assignment can be executed using assign1.sh file. 
```
usage: bash assign1.sh
```
- To excute individual program, separate shell scripts (.sh file) are also provided.


## question1 
```
usage: python3 q1.py
```
- modified-neighbor.json and data-all.json file is already provided.
- It outputs the mapping.json file which contains mapping for the districts name with their corresponding unique ids. This file is used by every program in the assignment to get district ids.


## question2
```
usage: bash case-generator.sh
```
- case-generator.sh excute the program q2.py which outputs the cases found positive in a week, month or in the entire time period of the analysis.
- Makes use of the data-all.json file(output by q1.py) and mapping.json file.
- It outputs 3 file: cases-week.csv, cases-month.csv, cases-overall.csv


## question3
```
usage: bash edge-generator.sh
```
- edge-generator.sh executes the program q3.py which outputs an undirected graph of districts.
- It requires mapping.json file and neighbor-districts-modified.json.
- It outputs edge-graph.csv which contains all the edges in the format (i,j) if an edge is present(is a neighboring district) between districts i and j. 


## question4
```
usage: bash neighbor-generator.sh
```
- neighbor-generator.sh executes the program q4.py which outputs the average and standard deviation of the number of cases of all neighboring districts of a district.
- It requires the output of program2 - cases-time.csv (cases file of a district) and mapping.json file.
- It outputs 3 files neighbor-time.csv where time is week, month, and overall.


## question5
```
usage: bash state-generator.sh
```
- state-generator.sh executes the program q5.py which outputs for a district, the average and standard deviation of the number of cases of all the other districts in the state.
- It requires the output of program2 - cases-time.csv (cases file of a district) and mapping.json file.
- It outputs 3 files state-time.csv where time is week, month, and overall.


## question6
```
usage: bash zscore-generator.sh
```
- state-generator.sh executes the program q6.py which outputs for a district, its z-score for every week, month, and overall, using separately the neighborhood and the state information.
- It requires the output of program2: cases-time.csv, output of program4: neighbor-time.csv, output of program5: state-time.csv and mapping.json file.
- It outputs 3 files zscore-time.csv where time is week, month, and overall.


## question7
```
usage: bash method-spot-generator.sh
```
- method-spot-generator.sh executes the program q7.py which outputs the hotspot and coldspot districts per week, per month, and overall.
- It requires the output of program2: cases-time.csv, output of program4: neighbor-time.csv, output of program5: state-time.csv and mapping.json file.
- It outputs 3 files method-spot-week.csv where time is week, month, and overall.


## question8
```
usage: bash top-generator.sh
```
- top-generator.sh executes the program q8.py which outputs the the top-5 hotspot and top-5 coldspot districts using the z-score values according to both the neighborhood and state methods.
- It requires the output of program6: zscore-time.csv.
- It outputs 3 files top-time.csv where time is week, month, and overall.

