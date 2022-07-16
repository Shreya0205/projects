#! /bin/bash

#PBS -q courses
#PBS -l nodes=4:ppn=4
#PBS -l walltime=00:10:00
#merge output and error into a single job_name.number_of_job_in_queue.
#PBS -j oe
#export fabric infiniband related variables
export I_MPI_FABRICS=shm:tmi
export I_MPI_DEVICE=rdma:OpenIB-cma
#change directory to where the job has been submitted from
cd $PBS_O_WORKDIR
#source paths
source /opt/software/intel17_update/initpaths intel64
#sort hostnames
sort $PBS_NODEFILE > hostfile.txt
#run the job on required number of cores

mpicc -o src src.c
for p in {1..15..1}
do
        echo "processing for process $p"

        for i in {1..5..1}
        do
                if [ "$i" == "1" ]; then
                         mpiexec -n $p -f hostfile.txt ./src.x 1 $p | tee >> data1/output_$p.txt
                else
                         mpiexec -n $p -f hostfile.txt ./src.x 1 $p 
                fi
        done

done

echo "data2 start"

for s in {1..15..1}
do
        echo "processing for process $s"
        for j in {1..5..1}
        do
                if [ "$j" == "1" ]; then
                         mpiexec -n $s -f hostfile.txt ./src.x 0 $j | tee >> data2/output_$s.txt
                else
                         mpiexec -n $s -f hostfile.txt ./src.x 0 $j 
                fi

        done

done




