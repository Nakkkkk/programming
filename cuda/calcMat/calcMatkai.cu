#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <helper_cuda.h>
#include <helper_timer.h>

#define N 1024 // 正方行列のサイズを指定（N×N）
#define BLOCK 16 // ブロックのサイズを指定

__global__ void
matrixMul(int* inMatA, int* inMatB, int* inMatC);

int main(int argc, char** argv){

    // 行列のサイズをバイト単位で算出
    int matrixSize = sizeof(unsigned int) * N * N;

    // ホスト側の行列変数設定
    int* hMatA;
    int* hMatB;
    int* hMatC;

    // 行列変数のメモリ確保
    hMatA = (int*)malloc(matrixSize);
    hMatB = (int*)malloc(matrixSize);

    // 初期値設定
    int col, row;
    for (col = 0; col < N; col++){
        for (row = 0; row < N; row++){
            hMatA[col * N + row] = rand() % (N * N);
            hMatB[col * N + row] = rand() % (N * N);
        }
    }

    // デバイス側の行列変数設定
    int* dMatA;
    int* dMatB;
    int* dMatC;

    // デバイスメモリ領域の確保
    cudaMalloc((void**)&dMatA, matrixSize);
    cudaMalloc((void**)&dMatB, matrixSize);
    cudaMalloc((void**)&dMatC, matrixSize);

    ////////////////////////////////////////////////////////////////////////
    StopWatchInterface *timer=NULL;
    sdkCreateTimer(&timer);
    sdkResetTimer(&timer);
    sdkStartTimer(&timer);

    // ホストからデバイスへの変数の受け渡し
    cudaMemcpy(dMatA, hMatA, matrixSize, cudaMemcpyHostToDevice);
    cudaMemcpy(dMatB, hMatB, matrixSize, cudaMemcpyHostToDevice);

    // ブロックサイズとグリッドサイズの設定
    dim3 block(BLOCK, BLOCK);
    dim3 grid( N / BLOCK, N / BLOCK);

    // カーネルの起動
    matrixMul<<<grid, block>>>(dMatA, dMatB, dMatC);
    cudaThreadSynchronize();

    // 結果の領域確保とデバイス側からのメモリ転送
    hMatC = (int*)malloc(matrixSize);
    cudaMemcpy(hMatC, dMatC, matrixSize, cudaMemcpyDeviceToHost);

    ////////////////////////////////////////////////////////////////////////
    sdkStopTimer(&timer);
    float time = sdkGetTimerValue(&timer);
    sdkDeleteTimer(&timer);
    printf("Processing time: %f (msec)\n", time);

    // ホスト・デバイスメモリの解放
    free(hMatA);
    free(hMatB);
    free(hMatC);
    cudaFree(dMatA);
    cudaFree(dMatB);
    cudaFree(dMatC);

    // 終了処理
    cudaThreadExit();
    //cutilExit(argc, argv);
}

__global__ void matrixMul(int* inMatA, int* inMatB, int* inMatC)
  {
  int col = blockIdx.x * blockDim.x + threadIdx.x;
  int row = blockIdx.y * blockDim.y + threadIdx.y;
  int scan;
  int target = 0;

  // 行列の演算を行う
  for (scan = 0; scan < N; scan++) {
      target += inMatA[col * N + scan] * inMatB[scan * N + row];
      __syncthreads();
  }

  inMatC[col * N + row] = target;
}
