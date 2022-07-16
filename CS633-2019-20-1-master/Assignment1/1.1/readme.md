CS633 Parallel Computing (Assignment 1)
--------------------------------------------------------------------------

The Assignment consists of two programs based on Blocking/Non-Blocking Send/Receive in MPI.
Program 1 will compute the effective bandwidth to send D data bytes 100 times from one node to another. Assignment is fully automated by executing run.sh file.
Entire program is taking around 7-8mins.



CONTENTS
---------------------
1. Hostfile.sh : A bash script to create a file of hosts which are up or live so that jobs never file (should be given executable permission).
2. run.sh : A bash script to automate the entire assignment from executing hostfile.sh to plot Boxplots for effective bandwidths (should be given executable permission).
3. src.c : Main Source code for implementing MPI_Send/Recvs of data bytes between two nodes.
4. Plot.py : A python file to plot effective bandwidths in the form of boxplots (MBps on y-axis and MB on x-axis) for each data point.
5. Plot.png : A sample plot showing the nature of the bandwidths for sending different data between 2 nodes with 1 process on each node.


PREREQUISITES
-----------------------------
1. MPICH
2. Python3
3. Matplotlib
4. Numpy


OBSERVATIONS
-----------------------------
1. Bandwidths are quite low (reaching upto 15MBps) from nodes csews40-csews53 due to network bottlenecks may be because of heavy jobs running on these nodes and because of that transfering is taking considerable amount of time to reach from one node to another. 
2. However, when the same program is executed on csews1-csews30, Bandwidths are as high upto 120 MBps.
3. Bandwidths are low in sample plot due to node from csews40.
4. The network itself has a data rate which serves as an upper bound on how many messages can be sent per quantum.
5. Application availability is usually not a concern for small message sizes as there is little to be gained while trying to overlap computation with communication when transfer times are relatively small. 
6. When messages sizes are large, there are overlapping computation with communication thats why bandwidth of larger message sizes matches with low data sizes or is even greater than small messages.


ISSUES
----------------
There were no such relevant issues as such faced during the implementation of Assignment1 (1.1).