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
        a[threadIdx.x] = b[threadIdx.x];
}

int main()
{
        char a[N] = "Hello \0\0\0\0\0\0";
        char b[N] = "World\0\0\0\0\0\0\0";

        char *ad;
        char *bd;
        const int size = N*sizeof(char);

        printf("%s\n", a);
        cudaError_t err;
        err = cudaMalloc( (void**)&ad, size );
	if (err != cudaSuccess) {
	  printf("cudaerror: %i\n", err);
	  return EXIT_FAILURE;
	}

        cudaMalloc( (void**)&bd, size );
        cudaMemcpy( ad, a, size, cudaMemcpyHostToDevice );

        dim3 dimBlock( blocksize, 1 );
        dim3 dimGrid( 1, 1 );
        copy<<<dimGrid, dimBlock>>>(ad, bd);
        cudaMemcpy( a, ad, size, cudaMemcpyDeviceToHost );
        cudaFree( ad );
        cudaFree( bd );

        printf("%s\n", a);
	if (strncmp(a, b, N)) {
	  printf("cuda kernel did not return expected result\n");
	  return EXIT_FAILURE;
	}
        return EXIT_SUCCESS;
}

