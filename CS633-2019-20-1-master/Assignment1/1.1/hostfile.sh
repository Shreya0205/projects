#!/bin/bash

for k in `seq 40 53`
do
        count=$(ssh csews$k uptime | grep load | wc -l)
        	
	if [ "$count" == "1" ]; then
		echo "csews$k:1" >> hostfile.txt
	fi

        length=$(wc -l hostfile.txt)
        if [ "$length" == "2 hostfile.txt" ]; then
		exit
        fi
done
