#include<stdio.h>
#include<malloc.h>
#include<stdlib.h>
#include<helper_cuda.h>

#define N 1024
#define BLOCK 16

__global__ void matrixMul(int* inMatA, int* inMatB, int* inMatC);

int main(int argc,char** argv){

  int matrixSize=sizeof((unsigned int)*N*N);

  int hMatA;
  int hMatB;
  int hMatC;

  hMatA=(int*)malloc(matrixSize);
  hMatB=(int*)malloc(matrixSize);

  int col,row;
  for(col=0;col<N;col++){
    for(row=0;row<N;row++){
      hMatA[col*N+row]=rand()%(N*N);
      hMatB[col*N+row]=rand()%(N*N);
    }
  }

  int dMatA;
  int dMatB;
  int dMatC;

  cudaMalloc((void**)&dMatA,matrixSize);
  cudaMalloc((void**)&dMatB,matrixSize);
  cudaMalloc((void**)&dMatC,matrixSize);

  cudaMemcpy(dMatA,hMatA,matrixSize,cudaMemcpyHostToDevice);
  cudaMemcpy(dMatB,hMatB,matrixSize,cudaMemcpyHostToDevice);

  dim3 block(BLOCK,BLOCK);
  dim3 grid(N/BLOCK,N/BLOCK);

  matrixMul<<<grid,block>>>(dMatA,dMatB,dMatC);
  cudaThreadSynchronize();

  hMatC=(int*)malloc(matrixSize);
  cudaMemcpy(hMatC,dMatC,matrixSize,cudaMemcpyDeviceToHost);

  free(hMatA);
  free(hMatB);
  free(hMatC);
  cudaFree(dMatA);
  cudaFree(dMatB);
  cudaFree(dMatC);

  cudaThreadExit();
  cutilExit(argc,argv);
}

__global__ void
matrixMul(int* inMatA,int* inMatB,int* inMatC){
  int col=blockIdx.x * blockDim.x + threadIdx.x;
  int row=blockIdx.y * blockDim.y + threadIdx.y;
  int scan;
  int target=0;

  for(scan=0;scan<N;scan++){
    target+=inMatA[col*N+scan]*inMatB[scan*N+row];
    __syncthreads();
  }

  inMatC[col*N+row]=target;
}
