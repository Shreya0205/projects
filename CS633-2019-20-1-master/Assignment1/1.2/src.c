#include <stdio.h>
#include <string.h>
#include "mpi.h"
#include <malloc.h>
#include <stdlib.h>

int main( int argc, char *argv[])
{
  int data = atoi(argv[1]);
  int option = atoi(argv[2]);

  char *arr = (char *)malloc(data * sizeof(char));

  int myrank, size,i,j,k;
  MPI_Status status;
  double start_time,total_time;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank( MPI_COMM_WORLD, &myrank );
  MPI_Comm_size( MPI_COMM_WORLD, &size );
  MPI_Request send_request, recv_request;
  
  start_time = MPI_Wtime ();
  
  if(option==1)
  {
	  if (myrank != 0) 
	  {    
	       for(i=0; i<100; i++)
	       MPI_Send(arr, data, MPI_CHAR, 0, 99, MPI_COMM_WORLD);
	  }
	  else 
	  {
	       char *recvarr[size];       
	       for (j=0; j<size; j++) 
	           recvarr[j] = (char *)malloc(data * sizeof(char)); 
	        
	       for(k=0;k<100;k++)
	       {
	          for (i=1; i<size; i++)
	          {
	            MPI_Recv(recvarr[i], data, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
	          } 
	       }
  	}   
  }
  else
  {
	 if(myrank!=0)
	  {
	     for(i=0; i<100; i++)
	     MPI_Isend(arr, data, MPI_BYTE, 0, 99, MPI_COMM_WORLD, &send_request);
	  }
	  else
	  {
	      char *recvarr[size];
	      for (j=0; j<size; j++)
	        recvarr[j] = (char *)malloc(data * sizeof(char));
	      
	      for(j=0; j<100; j++)
	      {
	         for (k=1; k < size; k++)
	         {
	            MPI_Irecv(recvarr[k], data, MPI_BYTE, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &recv_request);
	            MPI_Wait (&recv_request,&status);
	         }  
	      }
	       
   }
  }

if(myrank==0)
{
 total_time=MPI_Wtime()-start_time;
 printf ("%lf\n",((data*100)/(total_time*1000000))*(size-1));
}

MPI_Finalize();
return 0;
}
