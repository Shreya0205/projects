#!/bin/bash

for k in 11 12 14 15 16 26 27 28 29 30 42 43 44 46 56 57 58 59 60 72 73 74 75 76 87 88 89 90 103 104 105 106 107 117 118 119 120
do
        count=$(ssh 172.27.19.$k uptime | grep load | wc -l)

        if [ "$count" == "1" ]; then
                echo "172.27.19.$k" >> hostfile.txt
        fi

        length=$(wc -l hostfile.txt)
        if [ "$length" == "30 hostfile.txt" ]; then
                exit
        fi
done

