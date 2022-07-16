#include <stdio.h>
#include <mpi.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int Classify(double *means, double *items, int i, int k)
{
	double minDist=100000000000000000000000000.0;
	int index,u=0,z=0,v=0;
	double s=0;
	
	// calculating euclidean distance from every means 
	for(z=0;z<k;z++)
	{
		s=0;
		for(v=0;v<3;v++)
		{
			s=s+pow((items[i+v]-means[z*3+v]),2);
			//printf("\nyes");
		}
		s=sqrt(s);
		
		if(s<minDist)
		{
			minDist=s; 
			index=z;
		}
		
	}
        //return index of cluster whose mean is closest to the datapoint i
	return index;
}



void CalculateMeans(double *items, int k, int rank,int count)
{
    double *means = (double *)malloc(k*3*sizeof(double));
    int i=0,j=0,z=0;
    if(rank==0)
    {
       for(i=0;i<k*3;i++)
       {
	    //initialising means to intital data points
            means[i]=items[i];
       }
    }

    //clustersizes to store number of datapoints in a cluster
    int *clusterSizes = (int *)malloc(k*sizeof(int));
    for(i=0; i<k; i++)
           clusterSizes[i]=0;

    //sum stores sum of datapoints belonging to a cluster 
    double *sum = (double *)malloc(k*3*sizeof(double ));
    double *Gsums = NULL;
    int *GclusterSizes = NULL;

    if(rank==0)
    {
	    Gsums = malloc(k * 3 * sizeof(double));
            GclusterSizes = malloc(k * sizeof(double));
    }
    

    double iterations = 5;
    while(iterations > 1)
    {
	    for (i = 0; i < k*3; i++){ sum[i] = 0.0; }
            for (i = 0; i < k; i++) {clusterSizes[i] = 0;}
	    
	    
            MPI_Bcast(means,k*3,MPI_DOUBLE,0,MPI_COMM_WORLD);
	    
            int ind=0;  
            int u;
            
            // for every datapoint	    
	    for(i=0;i<count; i=i+3)
	    {
		         
		        ind = Classify(means, items, i, k);

			//increasing clustersize 
			clusterSizes[ind]++;

			for(z=0;z<3;z++)
			{
				sum[ind*3+z]=sum[ind*3+z]+items[i+z];
			}
	    }
            
	    //rank 0 gets sum and count of datapoints from all processes belonging to the same cluster
	    MPI_Reduce(sum, Gsums, k * 3, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            MPI_Reduce(clusterSizes, GclusterSizes, k, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

	   if(rank==0){
		    for (i = 0; i<k; i++)
                    {
                         for (j = 0; j<3; j++)
                         {
		             //taking average of datapoints
                             Gsums[3*i+j] /= GclusterSizes[i];
                         }
                    }
                    

                    for ( i=0; i<k*3; i++)
                    {
			 //updating means to new averages
                         means[i] = Gsums[i];
                    }
	    }
	   iterations--;
    }	    

    if(rank==0){
	    j=0;
	    printf("%d",k);
    for(i=0;i<k*3;i=i+3)
    {
            printf(",<%d,%f %f %f>",GclusterSizes[j],means[i],means[i+1],means[i+2]);
            j++;
    }
    printf("\n");}
}

int main(int argc, char **argv) {

    MPI_File in;
    int i=0,j=0,ts=0;
    int rank, size, count, kvalue;

    //argument1 to distinguish between data1 and data2
    int ch = atoi(argv[1]);
    int k[17],ts_max;

    // k values for data1 and data2
    int k1[17]={35,34,33,35,35,32,35,33,35,33,35,34,34,35,33,35,35};
    int k2[16]={50,51,50,53,50,50,50,50,51,50,51,52,52,50,50,50};
    FILE *fptr;

    if(ch){
	    for( i=0;i<17;i++)k[i]=k1[i];
	    //ts_max: number of datafiles
	    ts_max=17;
    }
    else{
	    for( i=0;i<16;i++)k[i]=k2[i];
	    ts_max=16;
    }
    
    double start1,start2,gstart,end1=0,end2=0,endpre=0,endproc=0,gend;
    MPI_Init(&argc, &argv);
    MPI_Status status;
    MPI_Offset filesize,proc_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    //argument2 for number of processes
    int P=atoi(argv[2]);
    if(rank==0)
    printf("Number of processes:%d\n",atoi(argv[2]));
    gstart=MPI_Wtime();
    
    for(ts=0; ts<ts_max; ts++)
    {
	char filename[17];
	if(ch)
	snprintf(filename, 14, "data1/file%d", ts);
	else
	snprintf(filename, 14, "data2/file%d", ts);
    
 	start1=MPI_Wtime();
    	double *buf2;
    	
    	MPI_File_open(MPI_COMM_WORLD, filename, MPI_MODE_RDONLY,MPI_INFO_NULL, &in);

    	MPI_File_get_size (in, &filesize);
    	filesize = filesize/(4*sizeof(double));
        if(rank==0)
	{ 
   		double* buf = (double*) malloc (filesize * sizeof (double));
    		MPI_File_read(in, buf, filesize, MPI_DOUBLE, &status);
    		buf2 = (double*) malloc (filesize * sizeof (double));
    
 		j=0;
    		for(i=0;i<filesize;i++)
    		{
			// skipping ids in array
            		if((i%4)!=0){
            		buf2[j]=buf[i];
            		j++;}
    		}
		
	 }
	// number of datapoints excluding ids
	proc_size=(filesize/4)*3;	
    	
    double* items = (double*) malloc (proc_size/size * sizeof (double));
    MPI_Scatter(buf2,proc_size/size, MPI_DOUBLE, items, proc_size/size, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    //count stores number of datapoints that a process have
    count=proc_size/size;
    
    end1=MPI_Wtime();
    endpre=endpre+end1-start1;
     
    MPI_Barrier(MPI_COMM_WORLD);   
    
    if(rank==0){
    printf("T%d:",ts+1);}
    kvalue=k[ts];
    start2=MPI_Wtime();

    //calculating means
    CalculateMeans(items,kvalue,rank,count);

    MPI_Barrier(MPI_COMM_WORLD);
    end2=MPI_Wtime();

    endproc=endproc+end2-start2;
    MPI_File_close(&in);
    
    }
    gend=MPI_Wtime();
    double ok,ok1;
    MPI_Reduce(&endpre,&ok,1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&endproc,&ok1,1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    if(rank==0){
    ok=ok/ts_max;
    ok1=ok1/ts_max;
    double ok2=gend-gstart;
    if(ch){
    fptr = fopen("data1/datafile1.txt","a");
    fprintf(fptr,"%f\n",ok);
    fclose(fptr);
    fptr = fopen("data1/datafile2.txt","a");
    fprintf(fptr,"%f\n",ok1);
    fclose(fptr);
    fptr = fopen("data1/datafile3.txt","a");
    fprintf(fptr,"%f\n",ok2);
    fclose(fptr);}
    else{
	     fptr = fopen("data2/datafile1.txt","a");
    fprintf(fptr,"%f\n",ok);
    fclose(fptr);
    fptr = fopen("data2/datafile2.txt","a");
    fprintf(fptr,"%f\n",ok1);
    fclose(fptr);
    fptr = fopen("data2/datafile3.txt","a");
    fprintf(fptr,"%f\n",ok2);
    fclose(fptr);}

    printf("Average time to pre-process:%f\n",ok);
    printf("Average time to process:%f\n",ok1);
    printf("Total Time:%f\n",ok2);
    }
    MPI_Finalize();
    
    return 0;
}
