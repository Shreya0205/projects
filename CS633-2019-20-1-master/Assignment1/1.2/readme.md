CS633 Parallel Computing (Assignment 1)
--------------------------------------------------------------------------

The Assignment consists of two programs based on Blocking/Non-Blocking Send/Receive in MPI.
Program 2 will compute the effective bandwidth to send D data bytes 100 times from many node to another. It consists of two parts i.e by Blocking Send/Recvs and Non-Blocking Send/Recvs.
Data is sent from N-1 nodes to a single node. The entire execution of program is taking about 45 mins.



CONTENTS
---------------------
1. Hostfile.sh : A bash script to create a file of hosts which are up or live so that jobs never fail.
2. run.sh : A bash script to automate the entire assignment from executing hostfile.sh to plot Boxplots for effective bandwidths.
3. src.c : Main Source code for implementing blocking and nonblocking Send/Recvs of data bytes between nodes.
4. Plot.py : A python file to plot effective bandwidths in the form of boxplots (MBps on y-axis and MB on x-axis) for each data point.
5. Plot.png : A sample plot showing the nature of the bandwidths for sending different data between nodes with 4 process on each node.


PREREQUISITES
-----------------------------
1. MPICH
2. Python3
3. Matplotlib
4. Numpy


OBSERVATIONS
-----------------------------
1. Bandwidths of non blocking calls are coming to be higher than blocking system calls because these non blocking calls return immediately (i.e., they do not block) even if the communication is not finished yet.
2. The non-blocking send and receive calls are the primary means of achieving overlap so bandwidths are somewhat higher than blocking.
3. With increasing data sizes, non blocking calls are efficient.
4. As nodes used are from csews40 to csews53, bandwidths are not very high as in nodes 1-25(~300MBps) but still reaches 60MBps.
5. With increasing number of processes, bandwidths are also increasing because there is simultaneous use of parallel resources.


ISSUES
----------------
<<<<<<< HEAD:Assignment1/1.2/readme.md
1. Need to use Heap Allocation because the program was not able to run because of bad termination error for largest data size and that the stack is not able to store it and even after setting stack size to unlimited, this problem still persists.
=======
1. Need to use Heap Allocation because the program was not able to run because of bad termination error for largest data size and that the stack is not able to store it and even after setting stack size to unlimited, this problem still persists.
>>>>>>> efce94d3e7200287e0d465873c42d9b0401f8e73:Assignment1/1.2/readme
