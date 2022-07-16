#!/bin/bash

mpicc -o src src.c

./hostfile.sh

for i in 1024 65536 262144 1048576
do
	for j in {1..5..1}
	do
		 mpiexec -n 8 -f hostfile1.txt ./src $i 1 | tee >> datafile1.txt
                 mpiexec -n 8 -f hostfile1.txt ./src $i 2 | tee >> datafile2.txt
		 mpiexec -n 16 -f hostfile2.txt ./src $i 1 | tee >> datafile3.txt
                 mpiexec -n 16 -f hostfile2.txt ./src $i 2 | tee >> datafile4.txt
		 mpiexec -n 32 -f hostfile3.txt ./src $i 1 | tee >> datafile5.txt
                 mpiexec -n 32 -f hostfile3.txt ./src $i 2 | tee >> datafile6.txt
	done
done

python3 plot.py 


