
#include <stdio.h>
#include <string.h>
#include "mpi.h"
#include <stdlib.h>

int main( int argc, char *argv[])
{
 
  int data = atoi(argv[1]);
  int  myrank, size,i=0;
  char arr[data];

  MPI_Status status;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank( MPI_COMM_WORLD, &myrank );
  MPI_Comm_size( MPI_COMM_WORLD, &size );

  double stime=MPI_Wtime();

  for(i=0;i<100;i++)
  {
  	if (myrank == 0) 
  	{ 
    		MPI_Send(arr, data , MPI_BYTE, 1, 99, MPI_COMM_WORLD);
       	}
  	else 
  	{		
		MPI_Recv(arr, data , MPI_BYTE, 0, 99, MPI_COMM_WORLD, &status);
  	}
  }

  if(myrank==1)
  printf("%lf\n", (sizeof(arr)*100/((MPI_Wtime() - stime)*1000000)));

  MPI_Finalize();
  
  return 0;
}


