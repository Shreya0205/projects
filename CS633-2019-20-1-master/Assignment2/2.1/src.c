#include <stdio.h>
#include <string.h>
#include "mpi.h"
#include <stdlib.h>

int main( int argc, char *argv[])
{
 
  int count = atoi(argv[1]);
  int myrank, size, x;
  char *arr = (char *)malloc(count * sizeof(char));
  char *recvarr = (char *)malloc(count * sizeof(char));
  double stime, endtime, buffer;

  MPI_Status status;
  MPI_Init(&argc, &argv);
  MPI_Request request[2];
  
  MPI_Comm_rank( MPI_COMM_WORLD, &myrank );
  MPI_Comm_size( MPI_COMM_WORLD, &size );
  

  for(int i=0; i < size; i++)
  {
        x = 10;
        while(myrank >= x)
            x *= 10;

        int tag = myrank*x + i;

        x = 10;
        while(i >= x)
            x *= 10;

	int tag2 = i*x + myrank;
	int color = tag2;
	
        
	stime = MPI_Wtime();
  	MPI_Sendrecv(arr, count, MPI_CHAR, i, tag, recvarr, count, MPI_CHAR, i, tag2, MPI_COMM_WORLD, &status);
	endtime = (MPI_Wtime() - stime)/2;
	
	//printf("%d --> %d send complete in %lf\n",myrank,i,endtime);
	//printf("myrank %d ---------- %d --> %d receive complete in %lf\n",myrank,i,myrank,endtime);
		
	MPI_Isend(&endtime, 1, MPI_DOUBLE, i, tag, MPI_COMM_WORLD,&request[0]);
	MPI_Irecv(&buffer, 1, MPI_DOUBLE, i, tag2, MPI_COMM_WORLD,&request[1]);
	MPI_Waitall(2,request,&status);
	
	//if(myrank==i) // to make diagonal bandwidth 0
	//	printf("%d %d %lf\n",myrank,i,0);
	//else{
		if( buffer > endtime)
			printf("%d %d %lf\n",myrank,i,count/(buffer*1000000));
		else
			printf("%d %d %lf\n",myrank,i,count/(endtime*1000000));
	//}

  }

 
  
  MPI_Finalize();
  
  return 0;
}


