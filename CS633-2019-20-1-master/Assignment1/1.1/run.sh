#!/bin/bash

mpicc -o src src.c

./hostfile.sh

for i in 128 1024 65536 1048576 4194304
do
	for j in {1..5..1}
	do
		 mpiexec -n 2 -f hostfile.txt ./src $i | tee >> datafile.txt
	done
done

python3 plot.py

