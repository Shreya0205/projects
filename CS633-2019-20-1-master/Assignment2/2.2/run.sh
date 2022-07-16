#!/bin/bash

mpicc -o src src.c

./hostfile.sh

for s in 8 16 32
do
	echo "Bandwidth,Algo,Datasizes,ppn" > datafile$s.csv
	for i in 2 4 8
	do
		for k in 64000 256000 512000 2000000 4000000
		do
			for j in {1..10..1}
			do
				 mpiexec -n $s -ppn $i -f hostfile.txt ./src $k $i | tee >> datafile$s.csv
			done
		done
	done
done

python3 plot.py 8
python3 plot.py 16
python3 plot.py 32
