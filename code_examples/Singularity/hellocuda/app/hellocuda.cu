// This is the REAL "hello world" for CUDA!
// It takes the string "Hello ", prints it, then passes it to CUDA with an array
// of offsets. Then the offsets are added in parallel to produce the string "World!"
// By Ingemar Ragnemalm 2010

#include <stdio.h>

const int N = 16;
const int blocksize = 16;

__global__
void copy(char *a, char *b)
{
        b[threadIdx.x] = a[threadIdx.x];
}


void printDeviceInfo() {
  int nDevices;

  auto err = cudaGetDeviceCount(&nDevices);
  if (err != cudaSuccess) {
    printf("cudaGetDeviceCount failed, cudaerror: %i\n", err);
    return;
  }
  for (int i = 0; i < nDevices; i++) {
    cudaDeviceProp prop;
    auto err = cudaGetDeviceProperties(&prop, i);
    if (err != cudaSuccess) {
      printf("cudaGetDeviceProperties failed, cudaerror: %i\n", err);
      return;
    }
    printf("Device Number: %d\n", i);
    printf("  Device name: %s\n", prop.name);
    printf("  Memory Clock Rate (KHz): %d\n",
           prop.memoryClockRate);
    printf("  Memory Bus Width (bits): %d\n",
           prop.memoryBusWidth);
    printf("  Peak Memory Bandwidth (GB/s): %f\n\n",
           2.0*prop.memoryClockRate*(prop.memoryBusWidth/8)/1.0e6);
  }
}


int main()
{
  printDeviceInfo();
        char a[N] = "World\0\0\0\0\0\0\0";
        char b[N] = "Not Working\0\0\0\0";

        char *ad;
        char *bd;
        const int size = N*sizeof(char);

        printf("input: %s\n", a);
        cudaError_t err;
        err = cudaMalloc( (void**)&ad, size );
	if (err != cudaSuccess) {
	  printf("cudaerror: %i\n", err);
//	  return EXIT_FAILURE;
	}

        cudaMalloc( (void**)&bd, size );
        cudaMemcpy( ad, a, size, cudaMemcpyHostToDevice );
        cudaMemcpy( bd, b, size, cudaMemcpyHostToDevice );

        dim3 dimBlock( blocksize, 1 );
        dim3 dimGrid( 1, 1 );
        copy<<<dimGrid, dimBlock>>>(ad, bd);
        cudaMemcpy( b, bd, size, cudaMemcpyDeviceToHost );
        cudaFree( ad );
        cudaFree( bd );

        printf("Hello %s\n", b);
	if (strncmp(a, b, N)) {
	  printf("cuda kernel did not return expected result\n");
	  return EXIT_FAILURE;
	}
        return EXIT_SUCCESS;
}

