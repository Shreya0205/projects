#!/bin/bash

mpicc -o src src.c -lm

./hostfile.sh

for p in {1..15..1}
do
	echo "processing for process $p"
	for i in {1..5..1}
	do
		if [ "$i" == "1" ]; then
			 mpiexec -n $p -f hostfile.txt ./src 1 $p | tee >> cse/data1/output_$p.txt
		else
			 mpiexec -n $p -f hostfile.txt ./src 1 $p > /dev/null
                fi

	done
	
done
echo "plotting graphs for data1"

python3 plot.py 1 

echo "data2 start"

for s in {1..15..1}
do
        echo "processing for process $s"
        for j in {1..5..1}
        do
                if [ "$j" == "1" ]; then
                         mpiexec -n $s -f hostfile.txt ./src 0 $j | tee >> cse/data2/output_$s.txt
                else
                         mpiexec -n $s -f hostfile.txt ./src 0 $j > /dev/null
                fi

        done

done
echo "plotting graphs for data2"

python3 plot.py 0





