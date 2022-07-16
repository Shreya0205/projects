#!/bin/bash

for k in `seq 40 54`
do
        count=$(ssh 172.27.19.$k uptime | grep load | wc -l)

        if [ "$count" == "1" ]; then
                echo "172.27.19.$k:4" >> hostfile.txt
        fi

        length=$(wc -l hostfile.txt)
        if [ "$length" == "2 hostfile.txt" ]; then
                cp hostfile.txt hostfile1.txt
        elif [ "$length" == "4 hostfile.txt" ]; then
                cp hostfile.txt hostfile2.txt
        elif [ "$length" == "8 hostfile.txt" ]; then
                cp hostfile.txt hostfile3.txt
                exit
        fi
done

