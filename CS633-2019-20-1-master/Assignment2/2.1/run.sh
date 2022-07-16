#!/bin/bash

mpicc -o src src.c

./hostfile.sh

for i in {1..10..1}
do
        for j in 64000 512000 2000000
        do
                 mpiexec -n 30 -ppn 1 -f hostfile.txt ./src $j | tee >> datafile$j.txt
        done
done


sort datafile64000.txt -t " " -k1,1n -k2,2n -o datafile64000.txt
sort datafile512000.txt -t " " -k1,1n -k2,2n -o datafile512000.txt
sort datafile2000000.txt -t " " -k1,1n -k2,2n -o datafile2000000.txt

python3 plot.py 64000
rm datafile.txt
python3 plot.py 512000
rm datafile.txt 
python3 plot.py 2000000
rm datafile.txt

