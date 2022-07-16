#include <stdio.h>
#include <string.h>
#include "mpi.h"
#include <stdlib.h>

int main( int argc, char *argv[])
{
 
  int count = atoi(argv[1]);
  int n = atoi(argv[2]);
  int myrank, size,i=0,root=0,send_index,recv_index,send_rank,recv_rank;
  double stime, endtime, oldtime, newtime;
  MPI_Status status;
  MPI_Datatype type;

  MPI_Init(&argc, &argv);

  MPI_Comm_rank( MPI_COMM_WORLD, &myrank );
  MPI_Comm_size( MPI_COMM_WORLD, &size );
  MPI_Request req[2];
  MPI_Status stats[2];
  
  count = count/4;

  float *arr = (float *)malloc(count * sizeof(float));
  float *recvarr = (float *)malloc(count * sizeof(float));
  

  MPI_Type_contiguous( count/size, MPI_FLOAT, &type );
  MPI_Type_commit(&type);
    
  if(myrank==0)
  {
  	for(i=0; i<count; i++)
		arr[i] = rand();
  }
  
  stime = MPI_Wtime();
  MPI_Bcast(arr, count, MPI_FLOAT, 0, MPI_COMM_WORLD);
  endtime = MPI_Wtime() - stime;
  MPI_Reduce(&endtime, &oldtime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
  if(myrank==0)
	  printf("%lf,Old_Bcast,%f,%d\n",(((count*4)/oldtime)/1000000)*(size-1),(count*4.0)/1000000,n);
  

  MPI_Barrier(MPI_COMM_WORLD);


  stime=MPI_Wtime();
  MPI_Scatter(arr, count/size, MPI_FLOAT, recvarr, count/size, MPI_FLOAT, 0, MPI_COMM_WORLD);
  count=count/size;
  memcpy (recvarr + count*myrank, recvarr, 4*count); 
 
  for(i=0;i<size-1;i++)
  {
  	send_rank = (myrank+1)%size;
	recv_rank = myrank-1;
	if(recv_rank == -1)
		recv_rank = size-1;
	
	send_index = (myrank - i)*count;
	if(send_index < 0)
		send_index = (myrank -i + size)*count;

	recv_index = (myrank -1 - i)*count;
	
	if(recv_index < 0)
		recv_index = (myrank -1 -i + size)*count;
		
	MPI_Isend(&recvarr[send_index], 1, type, send_rank, 0, MPI_COMM_WORLD, &req[0]);
        MPI_Irecv(&recvarr[recv_index], 1, type, recv_rank, 0, MPI_COMM_WORLD, &req[1]);
	MPI_Waitall(2,req,stats);
  }

  
  endtime = MPI_Wtime() - stime;
  MPI_Reduce(&endtime, &newtime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
  if(myrank==0)
          printf("%lf,New_Bcast,%f,%d\n",(((count*4*size)/newtime)/1000000)*(size-1),(count*4.0*size)/1000000,n);
  
 
  MPI_Finalize();
  free(recvarr);
  free(arr);
  return 0;
}
